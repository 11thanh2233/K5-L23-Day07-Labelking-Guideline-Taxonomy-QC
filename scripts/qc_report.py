"""Tính số liệu QC từ phiếu kiểm và GỢI Ý quyết định Hold / Rework / Release.

    python scripts/qc_report.py [--guideline-gap N] [--data-problem N]

--guideline-gap N : số ca bạn thấy guideline CHƯA có quy tắc (ca mơ hồ chưa chốt)  -> nếu > 0 gợi ý HOLD
--data-problem  N : số ảnh dữ liệu hỏng/mờ không dùng được                          -> nếu > 0 gợi ý HOLD

Ghi submission/qc/qc_report_auto.md. Bản QC_REPORT.md cuối cùng do NHÓM tự viết dựa trên bản auto này.
"""
from __future__ import annotations

import argparse
import json
from collections import Counter, defaultdict

from common import QC_DIR, die, load_coco, load_taxonomy, read_csv, rel

VALID = ["khong", "bo_sot", "thua", "sai_lop", "sai_vi_tri_kich_thuoc", "sai_thuoc_tinh"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--guideline-gap", type=int, default=0)
    ap.add_argument("--data-problem", type=int, default=0)
    args = ap.parse_args()
    tax = load_taxonomy()
    r = tax.rules
    for f in ("qc_sample.csv", "qc_review.csv", "labels_calibrated.json"):
        if not (QC_DIR / f).exists():
            die(f"Thiếu submission/qc/{f}. Chạy qc_sample.py và điền qc_review.csv trước.")
    sample = read_csv(QC_DIR / "qc_sample.csv")
    review = read_csv(QC_DIR / "qc_review.csv")
    lab = load_coco(QC_DIR / "labels_calibrated.json", tax)
    iaa = json.loads((QC_DIR / "iaa_summary.json").read_text(encoding="utf8")) if (QC_DIR / "iaa_summary.json").exists() else None

    sample_imgs = [s["image"] for s in sample]
    n_img = len(sample_imgs)
    n_obj = sum(int(s["so_doi_tuong"]) for s in sample)
    warns = []
    checked, err_rows = set(), []
    for i, row in enumerate(review, 2):
        img, et = (row.get("image") or "").strip(), (row.get("error_type") or "").strip().lower()
        if img not in sample_imgs:
            warns.append(f"Dòng {i} của qc_review.csv: ảnh '{img}' không nằm trong mẫu (bỏ qua).")
            continue
        if not et:
            continue
        if et not in VALID:
            warns.append(f"Dòng {i}: error_type '{et}' sai chính tả (chỉ nhận {', '.join(VALID)}) - dòng bị bỏ qua.")
            continue
        checked.add(img)
        oid = (row.get("object_id") or "").strip()
        if oid and oid.isdigit() and not any(o.id == int(oid) for o in lab.objects.get(img, [])):
            warns.append(f"Dòng {i}: object_id {oid} không có trong ảnh {img}.")
        if et != "khong":
            err_rows.append((img, oid or f"(dòng {i})", et))
    unchecked = [i for i in sample_imgs if i not in checked]
    if unchecked:
        warns.append(f"{len(unchecked)} ảnh trong mẫu CHƯA được kiểm (chưa có error_type): "
                     f"{', '.join(unchecked[:8])}{' ...' if len(unchecked) > 8 else ''}")

    err_objs = {(i, o) for i, o, _ in err_rows}
    err_imgs = {i for i, _, _ in err_rows}
    types = Counter(t for _, _, t in err_rows)
    ex = defaultdict(list)
    for i, _, t in err_rows:
        if i not in ex[t]:
            ex[t].append(i)
    n_err = len(err_rows)
    rate_obj = len(err_objs) / n_obj if n_obj else None
    rate_img = len(err_imgs) / n_img if n_img else None
    top3 = types.most_common(3)
    systematic = bool(top3 and n_err >= 3 and top3[0][1] >= 3 and top3[0][1] / n_err >= 0.5)

    iaa_pass = None if not iaa else iaa["overall"].get("pass")
    reasons = []
    if args.guideline_gap > 0 or args.data_problem > 0:
        decision = "HOLD"
        reasons.append(f"guideline chưa rõ ({args.guideline_gap} ca) / dữ liệu có vấn đề ({args.data_problem} ảnh) "
                       "-> tạm giữ để làm rõ")
    else:
        rw = []
        if rate_img is not None and rate_img > r["error_rate_img_max"]:
            rw.append(f"tỉ lệ ảnh có lỗi {rate_img * 100:.1f}% > {r['error_rate_img_max'] * 100:.0f}%")
        if systematic:
            rw.append(f"lỗi hệ thống: '{top3[0][0]}' chiếm {top3[0][1]}/{n_err} lỗi")
        if iaa_pass is False:
            rw.append("IAA (đo trước calibration) dưới ngưỡng")
        decision = "REWORK" if rw else "RELEASE"
        reasons = rw or [f"tỉ lệ ảnh lỗi {0 if rate_img is None else rate_img * 100:.1f}% <= "
                         f"{r['error_rate_img_max'] * 100:.0f}%, không lỗi hệ thống, IAA đạt"]
    if unchecked:
        reasons.append("LƯU Ý: còn ảnh mẫu chưa kiểm -> kết luận chưa đáng tin")

    def pc(a, b):
        return "n/a" if not b else f"{a}/{b} = {a / b * 100:.1f}%"
    L = ["# Báo cáo QC tự động (nháp)", "",
         "> Đây là **gợi ý** do script tính - người kiểm phải xác nhận. Script chỉ đếm theo phiếu kiểm bằng mắt người; "
         "không tự biết box có ôm sát vật hay không.", "",
         "## Mẫu", f"- Cỡ mẫu: {n_img} ảnh ({sum(1 for s in sample if s['la_ca_kho'] == 'yes')} ca khó + "
         f"{sum(1 for s in sample if s['la_ca_kho'] != 'yes')} ngẫu nhiên), {n_obj} đối tượng; "
         f"tổng lô: {len(lab.images)} ảnh.", f"- Phiên bản taxonomy: {tax.version}", "",
         "## Số đo", "| Chỉ số | Giá trị | Mẫu số |", "|---|---|---|",
         f"| Tỉ lệ lỗi **theo đối tượng** | {pc(len(err_objs), n_obj)} | {n_obj} đối tượng trong mẫu "
         "(lỗi bỏ sót tính như 1 đối tượng lỗi) |",
         f"| Tỉ lệ **ảnh có lỗi** (dùng cho ngưỡng) | {pc(len(err_imgs), n_img)} | {n_img} ảnh trong mẫu |"]
    if iaa:
        o = iaa["overall"]
        L += [f"| IoU trung bình (IAA, trước calibration) | {'n/a' if o['mean_iou'] is None else '%.3f' % o['mean_iou']} "
              f"(ngưỡng {r['iaa_iou']}) | {o['n_matched_pairs']} cặp box ghép |",
              f"| Đồng thuận lớp (IAA) | {'n/a' if o['class_agreement'] is None else '%.1f%%' % (o['class_agreement'] * 100)} "
              f"(ngưỡng {r['iaa_class'] * 100:.0f}%) | {o['n_matched_pairs']} cặp box ghép |"]
    L += ["", f"Ngưỡng Release: ảnh có lỗi <= {r['error_rate_img_max'] * 100:.0f}% (đếm theo ảnh).", "",
          "## Top 3 loại lỗi"]
    if top3:
        L += ["| Loại lỗi | Số lỗi | Ảnh ví dụ |", "|---|---|---|"]
        L += [f"| {t} | {c} | {', '.join(ex[t][:3])} |" for t, c in top3]
    else:
        L.append("(không ghi nhận lỗi nào)")
    if systematic:
        L.append(f"\n**Lỗi hệ thống**: '{top3[0][0]}' lặp lại ({top3[0][1]}/{n_err} lỗi) -> cần sửa quy tắc/guideline, không chỉ sửa từng ảnh.")
    if warns:
        L += ["", "## Cảnh báo"] + [f"- {w}" for w in warns]
    L += ["", "## Gợi ý quyết định (người kiểm xác nhận)", f"**{decision}**", ""] + [f"- {x}" for x in reasons]
    L += ["", "Cây quyết định: Hold (guideline chưa rõ/dữ liệu hỏng) -> Rework (>ngưỡng, lỗi lặp, IAA thấp) -> Release."]
    text = "\n".join(L) + "\n"
    (QC_DIR / "qc_report_auto.md").write_text(text, encoding="utf8")
    print(text)
    print(f"Đã ghi {rel(QC_DIR / 'qc_report_auto.md')}. Hãy tự viết QC_REPORT.md dựa trên số liệu này (không ghi đè tự động).")


if __name__ == "__main__":
    main()
