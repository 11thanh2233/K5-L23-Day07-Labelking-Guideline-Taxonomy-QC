# Báo cáo QC — Labelking

Bản nhãn bàn giao: `submission/qc/labels_calibrated.json` (taxonomy v1.1), quyết định theo QC vòng 2. Vòng 1 giữ nguyên trong `submission/qc/reviews/round-01/`.

> **Minh bạch về cách làm (RULES.md — AI, Số liệu trung thực).** Nhãn sau calibration được sinh bằng script từ bản đồng thuận, áp bảng quyết định và guideline v1.1 (không vẽ lại từng ảnh trên CVAT). Phiếu QC vòng 1 và vòng 2 do trợ lý AI (Claude) đọc ảnh overlay và điền dưới mã reviewer 103; 103 cần xác nhận lại các dòng phiếu trước khi nộp. Chi tiết ở mục 3 và 5.

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: nhãn bounding box 2D (COCO 1.0) cho mô hình phát hiện người và phương tiện trên ảnh đường phố, dùng để thực hành đặc tả và QC trong Day 07. Lô 40 ảnh tuyển chọn nhiều ca biên (đám đông, xe chở xe, tượng, phản chiếu, xe ngoài taxonomy); chưa đại diện cho dữ liệu vận hành, không dùng để đánh giá mô hình thật.
- Nguồn và phép sử dụng dữ liệu: ảnh Wikimedia Commons, giữ ghi công và giấy phép theo `data/ATTRIBUTION.csv` (manifest ghi `author`, `license`, `source_url` cho từng ảnh).
- Manifest và checksum nhãn cuối: `submission/qc/batch_manifest.json` (SHA-256 `4a44ad899a7143fbb57175fe168c1ed48327fd6774168c96fdfe698cd7fc3417`); nhãn `labels_calibrated.json` SHA-256 `a6f23045835c92f67997c5f2a8149cc9393d758d561bae7189c9941cdd8523da` (khớp trường `labels.sha256` trong manifest).
- Guideline và taxonomy khi gán / khi bàn giao: khi gán độc lập dùng `guideline_v1.0_agreed.md` + `taxonomy.json` v1.0 (6 lớp); khi bàn giao dùng `guideline_v1.1_calibrated.md` + `taxonomy_v1.1.json` (8 lớp, thêm `bus`, `tuk_tuk`; giữ nguyên `rules`). Đổi taxonomy vì 103 ghi 8 vùng xe ngoài taxonomy trong `image_issues.csv`; loại thay đổi `semantic` (`guideline_change.json`).

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: 80/80 lượt (40 ảnh × 2 người, `assignment.csv`); 101 gán 26 ảnh, 102 và 103 mỗi người 27 ảnh; `validate_labels.py --all` sạch cả 3 file.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số: tổng 303 cặp box ghép (IoU ≥ 0.5, mọi cặp người gán trên ảnh chung); IoU TB 0.818 (ngưỡng 0.85) — chưa đạt; cùng lớp 94.1% = 285/303 (ngưỡng 95%) — chưa đạt. Theo cặp: 101–102 IoU 0.814, lớp 89.7% (105/117); 101–103 IoU 0.817, lớp 97.5% (116/119); 102–103 IoU 0.828, lớp 95.5% (64/67). Cùng `occluded_level` 45.5% (138/303); cùng `truncated` 58.4% (177/303).
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: 54/117 box chưa ghép (người A / người B, cộng mọi cặp); 0 box loại do ignore; 150 ca bất đồng vùng ignore. Tổng 648 ca bất thường trên 37/40 ảnh (`calibration_candidates.csv`), gồm 8 ca `can_review_anh` từ `image_issues.csv`.
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: img_013 (101, 102) — cả hai để ảnh gần như trống dù ảnh có 2 người đi bộ, 1 ô tô và 1 xe tay ga cao trên 20 px, sai R-13; IAA không bắt được vì không có box để ghép. Kiểm bằng cách mở ảnh gốc đối chiếu bảng ca khó; bản cuối đã có `person` ×2, `car` ×3, `motorcycle` (xem ảnh QC vòng 2).

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: 667 dòng trong `calibration_decisions.csv` — 648 ca IAA (C001–C648) và 19 ca nhật ký QC (Q01–Q19); mỗi dòng có rule `R-01`…`R-14` của v1.1, người chốt 103. Phân bố ca IAA: R-10 150, R-01 129, R-13 103, R-08/R-09 200, R-07 36, R-12 13, R-14 10, R-05 5, R-02 2. Cột `kiem_lai` ghi "chờ kiểm lại" cho ca IAA; kết quả kiểm lại thực tế là phiếu QC vòng 1 và vòng 2.
- Tác động v1.1 lên nhãn và ảnh: phạm vi cả lô 40/40 ảnh (thay đổi `semantic`, có quyết định `pham_vi=lo`). Mapping lớp: 6 lớp v1.0 giữ tên; thêm 8 `tuk_tuk` (img_004, 016, 035, 040) và 3 `bus` (img_009, 031, 040) từ `image_issues.csv`; xe đạp chuyển `ignore_region` (R-11); 14 box đổi lớp từ ca `sai_lop`; `truncated` tính lại theo mép ảnh (R-08); `can_review=false` trên toàn bộ nhãn cuối. Bản sửa áp bằng script, không sửa tay trên CVAT.
- Tham chiếu bằng chứng khi Rework: vòng 1 (`reviews/round-01/`, nhãn SHA-256 `7fff4a5c…`) → 19 lỗi ghi thành Q01–Q19 trong `calibration_decisions.csv` → sửa trong `labels_calibrated_15c5a57c4e2002d9.json` (12 ảnh: img_001, 003, 005, 006, 010, 011, 013, 019, 023, 036, 037, 040) → `build_final.py` → vòng 2 (`reviews/round-02/`). Đã đối chiếu bằng script: 28 ảnh còn lại giống hệt vòng 1.

## 4. Kết quả duyệt

- Vòng QC: 2
- Người review và ngày: 103, 2026-11-17 (phiếu điền với hỗ trợ AI, xem ghi chú đầu báo cáo)
- Đã duyệt / cả lô: 40/40 ảnh (duyệt toàn lô, `mode=full`)
- Ảnh lỗi / ảnh đã duyệt: vòng 2: 0/40 = 0.0%; vòng 1: 12/40 = 30.0%
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: vòng 2: 0/473 = 0.0%; vòng 1: 15/480 = 3.1%
- Vật bỏ sót, ảnh và vùng: vòng 2: 0; vòng 1: 3 — img_037 xe buýt [0,218,235,390] và [715,232,760,345] (R-12), img_023 xích lô [575,205,790,530] (R-11); đã thêm ở vòng 2.
- Ca khó / phần còn lại, lỗi lặp và ví dụ: vòng 1 ca khó 12/37 ảnh lỗi, phần còn lại 0/3. Lỗi lặp: xe đạp gán `motorcycle` 6 box (img_003 #24 #45, img_006 #91 #93 #94, img_010 #149); `truncated=no` cho vật bị mép dưới cắt 4 box (img_005 #62 #63, img_019 #220, img_040 #492) vì box dừng cách mép 3–5 px, vượt ngưỡng 2 px của R-08. Vòng 2 không còn lỗi (`round-02/qc_review.csv`).
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: máy chặn được — box `img_005` vượt mép ảnh 0.01 px do làm tròn (`build_final.py` báo "bbox không hợp lệ", đã sửa `xyxy_to_xywh` trong `scripts/common.py` và chạy lại `qc_compare.py`, 648 ca không đổi); cần người đọc ảnh — xe đạp bị gán `motorcycle` (img_006 #93): lớp hợp lệ trong taxonomy nên script không phát hiện, chỉ thấy khi nhìn ảnh.

## 5. Quyết định bàn giao

- Quyết định: Release
- Lý do, người nhận và phạm vi sử dụng: theo cây Hold → Rework → Release: không Hold (đủ bằng chứng, guideline v1.1 đã chốt, `--guideline-gap 0 --data-problem 0`); vòng 1 là Rework (30.0% ảnh lỗi > ngưỡng 2%, có lỗi lặp); sau khi sửa Q01–Q19, vòng 2 đạt 0/40 ảnh và 0/473 annotation lỗi, `qc_report.py --round 2` gợi ý RELEASE. Người nhận: coach Day 07 / nhóm huấn luyện thực hành; chỉ dùng cho bài thực hành phát hiện vật 2D trên lô 40 ảnh này.
- Nếu còn việc: (1) 103 xác nhận lại bằng mắt các dòng phiếu vòng 1–2 do AI điền, ưu tiên ảnh dày đặc img_003, 008, 021, 030; nếu thấy lỗi thì mở vòng 3. (2) Sửa bảng ca khó img_013, img_036, img_038 trong guideline v1.1 (v1.0 mô tả sai các ảnh này). (3) Thống nhất xử lý xe đạp: v1.1 dùng `ignore_region` (R-11), khác bản guideline của 103. (4) Cân nhắc nới ngưỡng R-08 lên 5 px.
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: ca Q08 → `calibration_decisions.csv` (img_006, R-11, xe đạp #93) → `reviews/round-01/qc_review.csv` dòng `img_006.jpg,93,sai_lop` → ảnh `work/review/round-02/img_006.jpg.png` cho thấy vùng đó là `ignore_region` → `labels_calibrated.json` không còn box `motorcycle` trên xe đạp của cô gái áo trắng; kết quả: khớp.
