# Submission — bài nhóm

## Repo bài nộp

Một nhóm **một repo public**: fork repo đề, đổi tên theo mẫu, mời cả nhóm làm collaborator.

| Mẫu tên repo | Ví dụ |
|---|---|
| `K4-L23-DAY07-[TenNhom]-GuidelineQC` | `K4-L23-DAY07-Alpha-GuidelineQC` |

Tên nhóm viết không dấu, không khoảng trắng; ghép các phần bằng dấu `-`. Theo hướng dẫn lớp nếu giảng viên đặt quy ước khác.

## Trước khi nộp

1. **Đổi dòng tiêu đề của `README.md`** (đủ mọi thành viên):
   ```markdown
   # Day 07 Lab — Nhóm Alpha: 22001234 - Nguyễn Văn A, 22005678 - Trần Thị B
   ```
2. Điền [TEAM.md](TEAM.md).
3. Nộp link repo lên LMS **https://aithucchien.vinuni.edu.vn** hoặc kênh giảng viên/coach chỉ định. Một thành viên nộp, ghi đủ MSHV cả nhóm.

Hạn nộp do giảng viên/coach thông báo.

## Cấu trúc bắt buộc

```text
README.md                        # dòng đầu: MSHV - Họ và tên của MỌI thành viên
TEAM.md                          # thông tin nhóm, commit chốt bài
data/ATTRIBUTION.csv             # giữ nguyên
submission/
├── taxonomy.json                # taxonomy của nhóm (đã sửa theo guideline v1.0)
├── guidelines/
│   ├── individual/              # guideline_<MSHV>_<HoTen>.md, MỖI thành viên một file
│   ├── guideline_v1.0_agreed.md # sau khi cả nhóm thống nhất
│   └── guideline_v1.1_calibrated.md   # sau calibration
├── labels/                      # <MSHV>_<HoTen>.json, MỖI thành viên một file
├── individual_notes/            # <MSHV>_<HoTen>.md, MỖI thành viên một file
└── qc/
    ├── assignment.csv
    ├── calibration_candidates.csv      # ảnh / nhãn cần calibration (script)
    ├── calibration_decisions.csv       # mỗi quyết định một dòng (học viên)
    ├── labels_calibrated.json / .csv   # tập nhãn sau calibration
    ├── qc_sample.csv, qc_review.csv
    └── QC_REPORT.md             # báo cáo QC
```

Các file sinh bởi script khác (`iaa_summary.*`, `image_scores.csv`, `consensus_draft.json`, `qc_report_auto.md`, `flagged_images.txt`, `labels_calibrated_flagged.json`) cũng giữ trong `submission/qc/`. **Không** commit thư mục `work/`.

Quy ước tên: `<MSHV>` là chữ số, `<HoTen>` không dấu viết liền (ví dụ `22001234_NguyenVanA`).

## Checklist trước khi nộp

- [ ] Repo **public**, tên đúng quy tắc, mở được khi chưa đăng nhập.
- [ ] Dòng tiêu đề `README.md` đã đổi, liệt kê đủ `MSHV - Họ và tên`; phần "Kết quả tóm tắt" trong `TEAM.md` đã điền.
- [ ] `TEAM.md` đã điền, có commit chốt bài.
- [ ] Mọi thành viên: có guideline cá nhân, file nhãn, ghi chú cá nhân và **ít nhất một commit** của mình.
- [ ] Mỗi ảnh được ≥ 2 người gán (nhóm 5 người: 3); `python scripts/validate_labels.py --all` sạch.
- [ ] `taxonomy.json` khớp `guideline_v1.0_agreed.md`; mục `rules` không bị đổi.
- [ ] `calibration_decisions.csv`: mỗi ảnh bị cờ có ≥ 1 dòng quyết định; nội dung đã vào `guideline_v1.1_calibrated.md`.
- [ ] `QC_REPORT.md` điền đủ 7 mục, tỉ lệ lỗi kèm mẫu số, có quyết định Release / Hold / Rework.
- [ ] `python scripts/check_submission.py` không còn `LỖI`.
- [ ] Không có secret, thư mục `work/` hay dữ liệu ngoài phạm vi.
- [ ] Đã nộp link repo trước hạn.
