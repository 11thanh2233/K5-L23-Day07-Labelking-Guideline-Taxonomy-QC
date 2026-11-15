# Rubric — 100 điểm

Điểm dựa trên **bằng chứng trong repo** và khả năng tái lập, không dựa vào việc IAA cao hay được Release. Một nhóm báo **Rework** trung thực, có phân tích, vẫn có thể được điểm tốt.

Bài nhóm, nhưng điểm có phần chấm **theo từng thành viên** (guideline cá nhân, nhãn cá nhân, ghi chú cá nhân, commit). Thành viên thiếu sản phẩm cá nhân hoặc không có commit bị tính điểm phần đó riêng, không lấy điểm của nhóm.

| Hạng mục | Điểm | Bằng chứng | Điều kiện mất điểm |
|---|---:|---|---|
| **1. Guideline cá nhân** | 15 | Mỗi người: phát hiện ca khó thật trong 40 ảnh, nêu ảnh (`img_0xx`) và quyết định (6); ngưỡng thuộc tính đo được, lớp có ví dụ / phản ví dụ (5); đủ 5 phần, rõ ràng (4). `individual/guideline_<MSHV>_<HoTen>.md` | Giống hệt v0; chỉ chép lại câu chữ chung chung; xem bản của nhau |
| **2. Guideline thống nhất và taxonomy** | 20 | Đủ 5 phần (5); mọi chỗ bất đồng giữa các bản cá nhân đã chốt kèm lý do (6); xử lý vật ngoài taxonomy, vật không thật, che / cắt mép, vật nhỏ / đám đông (5); `taxonomy.json` khớp guideline, tách đúng lớp và thuộc tính (4). `guideline_v1.0_agreed.md`, `taxonomy.json` | Hai quy tắc mâu thuẫn trong cùng file; `taxonomy.json` lệch guideline; đổi mục `rules` |
| **3. Chia việc và gán nhãn** | 15 | Mỗi ảnh ≥ 2 người gán (nhóm 5 người: 3), tải cân bằng (5); nhãn mỗi người qua `validate_labels` (5); đúng ảnh được giao, tuân guideline v1.0, dùng `can_review` hợp lý (5). `assignment.csv`, `labels/*.json` | Gán nhầm ảnh; thiếu nhãn một thành viên; sửa guideline giữa chừng; dùng mô hình gán nhãn |
| **4. IAA, calibration** | 25 | IAA đúng, nêu mẫu số, đối chiếu ngưỡng 0.85 / 95% (5); từ `calibration_candidates.csv` phân tích nguyên nhân (cùng lệch hay một người lệch) (5); **mỗi quyết định một dòng** trong `calibration_decisions.csv` (7); `guideline_v1.1_calibrated.md` và `labels_calibrated.json` nhất quán với quyết định (8) | Thiếu dòng quyết định cho ảnh bị cờ; quy tắc trong v1.1 không khớp nhãn cuối; số IAA bị sửa tay |
| **5. QC và báo cáo** | 15 | Mẫu và cách chọn, **hai cách đếm tỉ lệ lỗi kèm mẫu số** (4); top 3 loại lỗi kèm ảnh ví dụ, phát hiện lỗi lặp lại (4); quyết định theo cây Hold → Rework → Release khớp số liệu (4); phần "script kiểm được và không kiểm được" thực chất (3). `QC_REPORT.md` | Báo Release khi > 2% ảnh lỗi; chỉ ghi % không mẫu số; sao chép nguyên `qc_report_auto.md` |
| **6. Tái lập và hợp tác** | 10 | `check_submission.py` không còn `LỖI` (3); mọi thành viên có commit và ghi chú cá nhân `individual_notes/` (4); README đúng tiêu đề MSHV - Họ tên, `TEAM.md` đầy đủ, repo public (3) | Thiếu commit của một thành viên; secret hay thư mục `work/` bị commit |

## Quy đổi và trừ điểm

- **Thiếu thành phần** chỉ được chấm phần có bằng chứng; không tự giả định kết quả.
- **Tạo số liệu giả** (nhãn, IAA, dòng QC): bài bị chấm 0 ở phần liên quan và báo giảng viên.
- Nộp muộn, sai tên repo, nộp sai link: trừ điểm theo [RULES.md](RULES.md).
- Điểm IAA hay quyết định Release **không** cộng thêm điểm; chỉ chất lượng phân tích và tính nhất quán được chấm.
