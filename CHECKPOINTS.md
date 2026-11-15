# Checkpoints — Day 07

Bài **nhóm 2–5 người**, dự kiến **240 phút**. Các mốc tính từ lúc bắt đầu, là điểm tự kiểm tra tại lớp, **không phải hạn nộp**. Deadline do giảng viên/coach thông báo.

| Mốc | Mục tiêu | Tự kiểm tra |
|---|---|---|
| 0:15 | **CP0** Chuẩn bị | Repo public đã fork và clone; `TEAM.md` đã điền; cài được thư viện. |
| 0:50 | **CP1** Guideline cá nhân | Mỗi người đã push file của mình, có ca khó theo ảnh và ngưỡng đo được. |
| 1:20 | **CP2** Guideline thống nhất | `guideline_v1.0_agreed.md` đủ 5 phần; `taxonomy.json` khớp; sinh được nhãn CVAT. |
| 1:30 | Nghỉ | |
| 2:30 | **CP3** Gán nhãn | `assignment.csv` đúng K; mỗi người đã export nhãn; `validate_labels.py --all` sạch. |
| 2:50 | **CP4** IAA | Chạy `qc_compare.py`, đọc `iaa_summary.md`, xem ảnh `work/viz/`. |
| 3:30 | **CP5** Calibration | Mỗi quyết định một dòng; có v1.1; `build_final.py` ra `labels_calibrated.json`. |
| 4:00 | **CP6** QC và nộp | `QC_REPORT.md` có quyết định; ghi chú cá nhân; `check_submission.py` sạch; đã nộp link. |

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
