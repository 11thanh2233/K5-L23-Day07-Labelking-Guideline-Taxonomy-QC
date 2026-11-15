# Nhãn của từng thành viên

Mỗi thành viên **một file COCO 1.0** export từ CVAT: `<MSHV>_<HoTen>.json` (ví dụ `22001234_NguyenVanA.json`).
Chỉ chứa các ảnh được giao trong `submission/qc/assignments/<MSHV>.txt`. Chạy `python scripts/validate_labels.py --all` trước khi commit.
