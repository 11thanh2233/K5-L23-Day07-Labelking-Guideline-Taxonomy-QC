"""Lấy mẫu QC trên nhãn cuối (labels_calibrated.json) và tạo phiếu kiểm.

    python scripts/qc_sample.py --n 20 --seed 42

Mẫu = MỌI ảnh từng bị cờ (ca khó) + n ảnh ngẫu nhiên trong số ảnh không bị cờ.
(Lab nhỏ nên nới lỏng; quy tắc chuẩn của slide: lô < 500 ảnh kiểm 100%; lô lớn kiểm >= 10%, tối thiểu 50 ảnh, cộng mọi ca khó.)

Đầu ra: submission/qc/qc_sample.csv, submission/qc/qc_review.csv (phiếu kiểm để điền), work/review/<ảnh>.png (ảnh vẽ sẵn id từng vật).
"""
from __future__ import annotations

import argparse
import random

from common import (IMAGES_DIR, QC_DIR, WORK_DIR, die, list_images, load_coco, load_taxonomy, read_flagged, rel,
                    write_csv)
from drawing import PALETTE, draw_layers


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--n", type=int, default=20, help="Số ảnh ngẫu nhiên lấy thêm từ ảnh không bị cờ (mặc định 20)")
    ap.add_argument("--seed", type=int, default=42)
    ap.add_argument("--force", action="store_true", help="Ghi đè qc_review.csv đã có (CẨN THẬN: mất phần đã điền)")
    args = ap.parse_args()
    tax = load_taxonomy()
    p = QC_DIR / "labels_calibrated.json"
    if not p.exists():
        die("Chưa có submission/qc/labels_calibrated.json. Chạy `python scripts/build_final.py` trước.")
    lab = load_coco(p, tax)
    flagged = [i for i in read_flagged() if i in lab.objects]
    pool = sorted(i for i in lab.objects if i not in set(flagged))
    k = min(args.n, len(pool))
    if k < args.n:
        print(f"Chỉ có {len(pool)} ảnh không bị cờ -> lấy {k} ảnh.")
    rnd = sorted(random.Random(args.seed).sample(pool, k))
    sample = sorted(set(flagged) | set(rnd))
    nobj = lambda i: sum(1 for o in lab.objects[i] if o.cls != tax.ignore)  # noqa: E731
    write_csv(QC_DIR / "qc_sample.csv", ["image", "la_ca_kho", "so_doi_tuong"],
              [{"image": i, "la_ca_kho": "yes" if i in flagged else "no", "so_doi_tuong": nobj(i)} for i in sample])

    rv = QC_DIR / "qc_review.csv"
    if rv.exists() and not args.force:
        print(f"Giữ nguyên {rel(rv)} (đã tồn tại; dùng --force để tạo lại).")
    else:
        write_csv(rv, ["image", "object_id", "error_type", "reviewer", "note"],
                  [{"image": i, "object_id": "", "error_type": "", "reviewer": "", "note": ""} for i in sample])
        print(f"Đã tạo phiếu kiểm {rel(rv)}.")

    out = WORK_DIR / "review"
    out.mkdir(parents=True, exist_ok=True)
    for i in sample:
        if (IMAGES_DIR / i).exists():
            draw_layers(IMAGES_DIR / i, [("final", PALETTE[1], lab.objects[i])], tax, show_id=True,
                        title=i).save(out / (i.rsplit(".", 1)[0] + ".png"))
    total = len(lab.objects)
    n_obj = sum(nobj(i) for i in sample)
    print(f"Mẫu QC: {len(sample)}/{total} ảnh ({len(flagged)} ca khó + {k} ngẫu nhiên), {n_obj} đối tượng.")
    print(f"Ảnh để duyệt (có id từng vật): {rel(out)}/")
    print("Bước tiếp: mở ảnh trong work/review/, điền qc_review.csv (xem scripts/README.md), rồi `python scripts/qc_report.py`")


if __name__ == "__main__":
    main()
