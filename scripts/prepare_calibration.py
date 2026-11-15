#!/usr/bin/env python3
"""Chuẩn bị gói calibration cho CVAT: chỉ các ảnh bị cờ.

Tạo:
  work/calib/images/            ảnh bị cờ (upload làm Task mới trong CVAT)
  work/calib/consensus_flagged.json   nhãn đồng thuận NHÁP của riêng các ảnh đó
                                      (CVAT: Task -> Actions -> Upload annotations -> COCO 1.0)

Chạy sau `python scripts/qc_compare.py`:
    python scripts/prepare_calibration.py
"""
from __future__ import annotations

import json
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
QC = ROOT / "submission" / "qc"
OUT = ROOT / "work" / "calib"


def main() -> int:
    flagged_f = QC / "flagged_images.txt"
    draft_f = QC / "consensus_draft.json"
    if not flagged_f.exists() or not draft_f.exists():
        print("Chưa có flagged_images.txt / consensus_draft.json. Chạy `python scripts/qc_compare.py` trước.")
        return 2
    flagged = [l.strip() for l in flagged_f.read_text(encoding="utf8").splitlines() if l.strip()]
    if not flagged:
        print("Không có ảnh nào bị cờ: không cần calibration ảnh. (Vẫn nên xem lại iaa_summary.md.)")
        return 0
    (OUT / "images").mkdir(parents=True, exist_ok=True)
    for f in flagged:
        shutil.copy2(ROOT / "data" / "images" / f, OUT / "images" / f)
    d = json.loads(draft_f.read_text(encoding="utf8"))
    names = {Path(i["file_name"]).name for i in d["images"]}
    keep = {i["id"] for i in d["images"] if Path(i["file_name"]).name in set(flagged)}
    d["images"] = [i for i in d["images"] if i["id"] in keep]
    d["annotations"] = [a for a in d["annotations"] if a["image_id"] in keep]
    (OUT / "consensus_flagged.json").write_text(json.dumps(d, ensure_ascii=False), encoding="utf8")
    print(f"Đã chuẩn bị {len(flagged)} ảnh bị cờ + {len(d['annotations'])} box nháp trong work/calib/")
    print("  1) CVAT: tạo Task mới, upload work/calib/images/")
    print("  2) Actions -> Upload annotations -> COCO 1.0 -> work/calib/consensus_flagged.json")
    print("  3) Sửa theo quyết định calibration, Export COCO 1.0 -> submission/qc/labels_calibrated_flagged.json")
    miss = [f for f in flagged if f not in names]
    if miss:
        print("CẢNH BÁO: ảnh có cờ nhưng không có trong consensus_draft:", miss)
    return 0


if __name__ == "__main__":
    sys.exit(main())
