"""Gộp nhãn cuối sau calibration: ảnh không lệch lấy từ đồng thuận, ảnh bị cờ lấy từ bản đã calibration.

Chuẩn bị:
  1) Họp calibration, ghi mỗi quyết định MỘT dòng vào submission/qc/calibration_decisions.csv
     (lần đầu chạy script sẽ tự tạo file mẫu để điền).
  2) Sửa lại các ảnh bị cờ trong CVAT theo quyết định, export COCO 1.0 -> lưu thành
     submission/qc/labels_calibrated_flagged.json (chỉ cần chứa các ảnh bị cờ).

    python scripts/build_final.py
"""
from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from common import (QC_DIR, build_coco, die, load_coco, load_taxonomy, make_ann, read_csv, read_flagged, rel,
                    write_csv, xyxy_to_xywh)

DEC_COLS = ["case_id", "image", "quyet_dinh", "quy_tac_ghi_vao_guideline", "phien_ban_guideline", "nguoi_chot"]


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--calibrated", default=str(QC_DIR / "labels_calibrated_flagged.json"),
                    help="COCO sau calibration (chỉ ảnh bị cờ)")
    args = ap.parse_args()
    tax = load_taxonomy()
    cons_p, cand_p = QC_DIR / "consensus_draft.json", QC_DIR / "calibration_candidates.csv"
    if not cons_p.exists():
        die("Chưa có consensus_draft.json. Chạy `python scripts/qc_compare.py` trước.")
    flagged = read_flagged()
    dec_p = QC_DIR / "calibration_decisions.csv"

    if flagged and not dec_p.exists():
        rows = [{"case_id": c["case_id"], "image": c["image"]} for c in read_csv(cand_p)] if cand_p.exists() else []
        write_csv(dec_p, DEC_COLS, rows)
        print(f"Đã tạo file mẫu {rel(dec_p)} ({len(rows)} dòng, mỗi ca bất thường một dòng).\n"
              "Hãy điền cột quyet_dinh, quy_tac_ghi_vao_guideline, phien_ban_guideline, nguoi_chot "
              "(có thể gộp nhiều ca cùng quy tắc, thêm/xoá dòng tuỳ ý nhưng mỗi ảnh bị cờ cần >= 1 dòng đã điền), "
              "rồi chạy lại script này.")
        sys.exit(1)

    decs = [r for r in (read_csv(dec_p) if dec_p.exists() else []) if (r.get("quyet_dinh") or "").strip()]
    done_imgs = {r["image"].strip() for r in decs if (r.get("image") or "").strip()}
    errs = [f"Ảnh bị cờ {i} chưa có dòng quyết định nào (điền quyet_dinh trong calibration_decisions.csv)."
            for i in flagged if i not in done_imgs]
    warns = [f"Dòng {r.get('case_id') or r.get('image')}: thiếu quy_tac_ghi_vao_guideline / phien_ban_guideline."
             for r in decs if not (r.get("quy_tac_ghi_vao_guideline") or "").strip()
             or not (r.get("phien_ban_guideline") or "").strip()]

    cal_p = Path(args.calibrated)
    cal = None
    if flagged:
        if not cal_p.exists():
            errs.append(f"Chưa có {rel(cal_p)}: export COCO 1.0 từ CVAT sau khi sửa các ảnh bị cờ rồi lưu đúng tên này.")
        else:
            cal = load_coco(cal_p, tax)
            errs += [f"Ảnh bị cờ {i} không có trong file calibrated." for i in flagged if i not in cal.images]
            for p in cal.problems:
                warns.append(p)
            for o in (o for objs in cal.objects.values() for o in objs):
                if o.cls not in tax.classes:
                    errs.append(f"Lớp '{o.cls}' trong file calibrated không thuộc taxonomy.")
                    break
    for w in warns:
        print("[WARN]", w)
    if errs:
        for e in errs:
            print("[ERROR]", e)
        sys.exit(1)

    cons = load_coco(cons_p, tax)
    images, anns, csv_rows, aid = [], [], [], 1
    flagged_set = set(flagged)
    for img in sorted(cons.images):
        if img in flagged_set:
            src, objs, w, h = "calibration", cal.objects[img], *cal.images[img]
        else:
            src, objs, (w, h) = "consensus", cons.objects[img], cons.images[img]
        iid = len(images) + 1
        images.append({"id": iid, "file_name": img, "width": w, "height": h})
        for o in objs:
            if o.cls not in tax.classes:
                continue
            anns.append(make_ann(tax, aid, iid, o.cls, o.box, o.attrs))
            if o.cls != tax.ignore:
                bx = xyxy_to_xywh(o.box)
                csv_rows.append({"image": img, "class": o.cls, "x": bx[0], "y": bx[1], "w": bx[2], "h": bx[3],
                                 **{n: o.attrs[n] for n in tax.attrs if n != "can_review"}, "nguon": src})
            aid += 1
    (QC_DIR / "labels_calibrated.json").write_text(json.dumps(
        build_coco(tax, images, anns, {"description": "Nhãn cuối sau calibration", "taxonomy": tax.version}),
        ensure_ascii=False, indent=1), encoding="utf8")
    cols = ["image", "class", "x", "y", "w", "h"] + [n for n in tax.attrs if n != "can_review"] + ["nguon"]
    write_csv(QC_DIR / "labels_calibrated.csv", cols, csv_rows)
    n_cal = sum(1 for r in csv_rows if r["nguon"] == "calibration")
    print(f"Đã gộp {len(images)} ảnh, {len(anns)} annotation ({len(csv_rows)} vật + vùng ignore tách riêng): "
          f"{n_cal} vật từ calibration, {len(csv_rows) - n_cal} từ đồng thuận.")
    print(f"Ghi: {rel(QC_DIR / 'labels_calibrated.json')}, {rel(QC_DIR / 'labels_calibrated.csv')}")
    print("Bước tiếp: python scripts/qc_sample.py")


if __name__ == "__main__":
    main()
