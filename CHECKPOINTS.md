# Checkpoints — Day 07

Bài **nhóm 2–5 người**, dự kiến **240 phút**. Các mốc tính từ lúc bắt đầu, là điểm tự kiểm tra tại lớp, **không phải hạn nộp**. Deadline do giảng viên/coach thông báo.

| Mốc | Mục tiêu | Minh chứng / tự kiểm tra |
|---|---|---|
| 0:15 | **CP0 — Chuẩn bị** | Repo của nhóm đã fork, public, mọi người đã clone; `README.md` có tiêu đề `MSHV - Họ tên` đủ thành viên; `TEAM.md` đã điền; `pip install -r requirements.txt` chạy được. |
| 0:50 | **CP1 — Guideline cá nhân** | Mỗi người đã push `submission/guidelines/individual/guideline_<MSHV>_<HoTen>.md`: có ca khó theo ảnh (`img_0xx`), quyết định và ngưỡng đo được. Chưa ai xem bản của nhau. |
| 1:20 | **CP2 — Guideline thống nhất** | `guideline_v1.0_agreed.md` đủ 5 phần; mọi chỗ bất đồng đã chốt kèm lý do; `taxonomy.json` khớp guideline; `python scripts/make_cvat_labels.py` chạy được. |
| 1:30 | Nghỉ | |
| 2:30 | **CP3 — Chia việc và gán nhãn** | `assignment.csv` đúng K (2; nhóm 5 người là 3); mỗi người đã export `submission/labels/<MSHV>_<HoTen>.json`; `python scripts/validate_labels.py --all` không còn `LỖI`. |
| 2:50 | **CP4 — So sánh và IAA** | Chạy `qc_compare.py`; đọc `iaa_summary.md` (IoU, % cùng lớp, mẫu số); có `calibration_candidates.csv`; xem ảnh `work/viz/`. Mỗi nhóm bất thường đã đoán nguyên nhân (cùng lệch hay một người lệch). |
| 3:30 | **CP5 — Calibration** | `calibration_decisions.csv` có **mỗi quyết định một dòng**; `guideline_v1.1_calibrated.md`; `labels_calibrated_flagged.json`; `build_final.py` chạy xong ra `labels_calibrated.json`. |
| 4:00 | **CP6 — QC và nộp** | `qc_sample.csv`, `qc_review.csv` đã điền, `QC_REPORT.md` có quyết định Release / Hold / Rework; ghi chú cá nhân của mọi người; `python scripts/check_submission.py` hết `LỖI`; đã nộp link. |

## Chi tiết từng checkpoint

### CP1 · Cần hiểu
Chỗ nào v0 làm hai người hiểu khác nhau? Mức thuộc tính của bạn có **ngưỡng đo được** (ví dụ phần trăm che) chưa?

### CP2 · Cần hiểu
Phép thử lớp/thuộc tính: *"mô hình có phải đoán ra điều này không?"* Vật không thuộc lớp nào xử lý thế nào, và cả nhóm có **cùng một** cách không?

### CP3 · Cần hiểu
Vì sao phải gán độc lập? Script `validate_labels.py` kiểm được gì và **không** kiểm được gì (box có ôm sát vật không)?

### CP4 · Cần hiểu
IAA thấp: sửa guideline hay sửa người gán? Dựa vào dấu hiệu nào để phân biệt?

### CP5 · Cần hiểu
Quyết định nào là quy tắc mới phải vào guideline? Nếu thiếu dòng ghi quyết định, nhóm sẽ tranh luận lại đúng ca đó vào lần sau.

### CP6 · Cần hiểu
Tỉ lệ lỗi **theo đối tượng** khác **theo ảnh** thế nào, vì sao luôn ghi mẫu số? Cây quyết định đi theo thứ tự Hold → Rework → Release.

Chi tiết lệnh xem [GUIDE.md](GUIDE.md). Nếu CVAT chậm, mỗi người có thể cài CVAT local hoặc dùng tài khoản cvat.ai riêng từ trước buổi học.
