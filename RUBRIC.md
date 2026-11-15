# Rubric — 100 điểm

Điểm dựa trên **bằng chứng trong repo**, không dựa vào việc IAA cao hay được Release. Nhóm báo **Rework** trung thực, có phân tích, vẫn có thể được điểm tốt.

Bài nhóm, nhưng phần cá nhân chấm **theo từng người**: thiếu guideline cá nhân, nhãn, ghi chú hoặc commit thì bị tính riêng.

| # | Hạng mục | Điểm | Bằng chứng |
|---|---|---:|---|
| 1 | Guideline cá nhân | 15 | `individual/guideline_<MSHV>_<HoTen>.md` |
| 2 | Guideline thống nhất và taxonomy | 20 | `guideline_v1.0_agreed.md`, `taxonomy.json` |
| 3 | Chia việc và gán nhãn | 15 | `assignment.csv`, `labels/*.json` |
| 4 | IAA và calibration | 25 | `iaa_summary.md`, `calibration_*.csv`, `guideline_v1.1`, `labels_calibrated.json` |
| 5 | QC và báo cáo | 15 | `QC_REPORT.md`, `qc_review.csv` |
| 6 | Tái lập và hợp tác | 10 | `check_submission.py`, commit, `TEAM.md` |

## 1. Guideline cá nhân (15)
- 6: tìm ra ca khó **thật** trong 40 ảnh, nêu ảnh (`img_0xx`) và quyết định.
- 5: mức thuộc tính có ngưỡng đo được; lớp có ví dụ và phản ví dụ.
- 4: đủ 5 phần, rõ ràng.
- *Mất điểm:* giống hệt v0, chỉ chung chung, xem bản của nhau.

## 2. Guideline thống nhất và taxonomy (20)
- 5: đủ 5 phần.
- 6: mọi chỗ bất đồng giữa các bản cá nhân đã chốt, có lý do.
- 5: xử lý vật ngoài taxonomy, vật không thật, che / cắt mép, vật nhỏ / đám đông.
- 4: `taxonomy.json` khớp guideline; tách đúng lớp và thuộc tính.
- *Mất điểm:* hai quy tắc mâu thuẫn; `taxonomy.json` lệch guideline; đổi mục `rules`.

## 3. Chia việc và gán nhãn (15)
- 5: mỗi ảnh ≥ 2 người gán (nhóm 5 người: 3); tải cân bằng.
- 5: nhãn mỗi người qua `validate_labels`.
- 5: đúng ảnh được giao, theo guideline v1.0, dùng `can_review` hợp lý.
- *Mất điểm:* gán nhầm ảnh, thiếu nhãn một thành viên, sửa guideline giữa chừng, dùng mô hình gán nhãn.

## 4. IAA và calibration (25)
- 5: IAA đúng, nêu mẫu số, đối chiếu ngưỡng 0.85 / 95%.
- 5: phân tích nguyên nhân từng nhóm bất thường (cùng lệch hay một người lệch).
- 7: **mỗi quyết định một dòng** trong `calibration_decisions.csv`.
- 8: `guideline_v1.1` và `labels_calibrated.json` nhất quán với quyết định.
- *Mất điểm:* thiếu quyết định cho ảnh bị cờ; v1.1 không khớp nhãn cuối; sửa tay số IAA.

## 5. QC và báo cáo (15)
- 4: mẫu và cách chọn; **hai cách đếm tỉ lệ lỗi, kèm mẫu số**.
- 4: top 3 loại lỗi có ảnh ví dụ; nhận ra lỗi lặp lại.
- 4: quyết định theo cây Hold → Rework → Release, khớp số liệu.
- 3: phần "script kiểm được và không kiểm được" thực chất.
- *Mất điểm:* báo Release khi > 2% ảnh lỗi; chỉ ghi % không mẫu số; chép nguyên `qc_report_auto.md`.

## 6. Tái lập và hợp tác (10)
- 3: `check_submission.py` không còn `LỖI`.
- 4: mọi thành viên có commit và ghi chú cá nhân.
- 3: README đổi đúng tiêu đề MSHV - Họ tên, `TEAM.md` đầy đủ, repo public.
- *Mất điểm:* thiếu commit của một thành viên; commit `work/` hoặc secret.

## Trừ điểm chung
- Thiếu thành phần: chỉ chấm phần có bằng chứng.
- **Số liệu giả** (nhãn, IAA, dòng QC): 0 điểm phần liên quan, báo giảng viên.
- Nộp muộn, sai tên repo, sai link: theo [RULES.md](RULES.md).
