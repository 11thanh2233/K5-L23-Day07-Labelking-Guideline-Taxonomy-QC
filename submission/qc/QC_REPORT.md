# Báo cáo QC — Labelking

> Bản nháp sau Pha 4 (QC Lead 103, 2026-11-17). Mục 3–5 điền sau Pha 5–6.

## 1. Mục đích, dữ liệu và phiên bản

- Mục đích và giới hạn sử dụng: nhãn box 2D cho mô hình phát hiện người và phương tiện trên ảnh đường phố; 40 ảnh, chưa đại diện mọi điều kiện giao thông.
- Nguồn và phép sử dụng dữ liệu: ảnh Wikimedia Commons, giữ ghi công theo `data/ATTRIBUTION.csv`.
- Manifest và checksum nhãn cuối: chưa có (sinh ở Pha 5 bằng `build_final.py`).
- Guideline và taxonomy khi gán / khi bàn giao: gán theo `guideline_v1.0_agreed.md` (bản cuối commit `d2da869`: `motorcycle` gồm xe đạp). `taxonomy.json` có lớp khớp v1.0 nhưng trường `version` vẫn là `v0`, cần sửa.

## 2. Phân công và đồng thuận trước calibration

- Lượt hoàn thành / được giao: **80/80** (40 ảnh × 2 người, seed 42); `validate_labels.py --all` sạch.
- Số cặp box ghép, IoU TB, đồng thuận lớp và mẫu số:

  | Cặp | Cặp ghép | IoU TB (≥ 0.85) | Cùng lớp (≥ 95%) | Kết quả |
  |---|---|---|---|---|
  | Tổng | 303 | 0.818 | 94.1% (285/303) | Chưa đạt |
  | 101–102 | 117 | 0.814 | 89.7% (105/117) | Chưa đạt |
  | 101–103 | 119 | 0.817 | 97.5% (116/119) | Chưa đạt (IoU) |
  | 102–103 | 67 | 0.828 | 95.5% (64/67) | Chưa đạt (IoU) |

  Cùng `occluded_level`: 45.5% (138/303). Cùng `truncated`: 58.4% (177/303).
- Box chưa ghép, loại do ignore, bất đồng vùng ignore: chưa ghép 54 / 117 (người A / người B, cộng mọi cặp); loại do ignore: 0; bất đồng vùng ignore: 150 ca. Tổng 648 ca trên 37 ảnh (`calibration_candidates.csv`).
- Ca hai người có thể cùng sai sau khi đối chiếu tham chiếu: **img_013** (101, 102). Cả hai để ảnh trống, nhưng ảnh có 2 người đi bộ (~80 px), 1 ô tô, 1 xe tay ga đỗ → sai R-01/R-02. Nguyên nhân: bảng ca khó v1.0 mô tả sai ảnh này. Kiểm bằng cách mở ảnh gốc; IAA không bắt được vì không có box để ghép.

**Phân loại bất đồng (đầu vào họp Pha 5):**

| Nhóm | Bằng chứng | Loại | Hướng xử lý |
|---|---|---|---|
| `truncated` | 102 đặt `yes` 167/207 box, kể cả vật giữa ảnh; 101–103 khớp 95% | Một người lệch | 102 sửa nhãn |
| `person` → `car` | 102 ở img_025, img_008 (IoU 0.7–0.9); thêm img_029, img_031 | Một người lệch | 102 sửa nhãn |
| `occluded_level` | 37–59% ở cả 3 cặp | Guideline mơ hồ | v1.1 thêm ảnh mẫu từng mức |
| `ignore_region` | 150 ca, mọi cặp | Guideline mơ hồ (v1.0 vs bản đề xuất của 102) | Chốt quy tắc, kiểm lại cả lô |
| car / van / truck | img_005, img_016, img_028 | Guideline mơ hồ | Chốt pickup = `truck`, Hiace = `van` |
| Vật nhỏ hậu cảnh | 103 dư 76 box so với 101 | Guideline mơ hồ | Chốt ngưỡng "đủ rõ" |
| Bảng ca khó v1.0 | img_013, img_036, img_038 bị mô tả sai | Lỗi guideline | Sửa ở v1.1 |

## 3. Calibration và kiểm lại

- Ca đã xử lý, rule ID, bản sửa và người xác nhận: chưa có — `calibration_decisions.csv` (648 dòng) chờ họp Pha 5.
- Tác động v1.1 lên nhãn và ảnh: chưa có — chờ `guideline_v1.1_calibrated.md` và `guideline_change.json` (Người 2).
- Tham chiếu bằng chứng khi Rework: chưa có.

## 4. Kết quả duyệt

- Vòng QC: chưa có
- Người review và ngày: chưa có
- Đã duyệt / cả lô: chưa có
- Ảnh lỗi / ảnh đã duyệt: chưa có
- Annotation đối tượng hiện có bị lỗi / annotation đối tượng đã duyệt: chưa có
- Vật bỏ sót, ảnh và vùng: chưa có
- Ca khó / phần còn lại, lỗi lặp và ví dụ: chưa có
- Một lỗi máy chặn được và một lỗi cần người đọc ảnh: máy chặn được — `validate_labels.py` cảnh báo box nhỏ dưới 20 px (img_009, img_025, img_039); cần người đọc ảnh — img_013 bị bỏ trống bởi cả hai người.

## 5. Quyết định bàn giao

- Quyết định: chưa có (hiện tại là Hold vì IAA chưa đạt và chưa calibration)
- Lý do, người nhận và phạm vi sử dụng: chưa có
- Nếu còn việc: họp Pha 5 chốt 7 nhóm trên (cả nhóm); v1.1 và `guideline_change.json` (102); 102 sửa `truncated` và lớp `person`; điền `calibration_decisions.csv` (103).
- Kiểm ngược từ báo cáo tới ảnh, rule và nhãn: chưa có
