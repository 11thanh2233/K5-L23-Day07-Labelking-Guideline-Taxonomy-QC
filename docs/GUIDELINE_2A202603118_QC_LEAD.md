# Guideline Người 3 — QC Lead

Xương sống: `team_dashboard.html` (Người 3 = IAA, disagreement, calibration, QC, báo cáo).
Thay `<mã>` bằng mã của bạn. Chạy lệnh từ thư mục gốc repo.

## A. Việc chung (mọi thành viên)

| # | Việc | Lệnh / file | Xong khi |
|---|---|---|---|
| 1 | Đọc guideline v0 + quy tắc lab | `guideline/guideline_v0_starter.md`, `RULES.md` | Nắm được 5 lớp và 3 thuộc tính |
| 2 | Viết guideline cá nhân (độc lập) | `submission/guidelines/individual/guideline_<mã>.md` | Đủ 5 mục, mỗi ca khó có `img_0xx` |
| 3 | Kiểm ảnh được giao | `work/<mã>/images/`, `submission/qc/assignments/<mã>.txt` | Số ảnh khớp danh sách |
| 4 | Gán nhãn độc lập trên Task CVAT của mình | CVAT, guideline v1.0 | Không xem nhãn người khác |
| 5 | Lưu sau mỗi ảnh, kiểm lại box | CVAT `Save` | Box ôm sát phần nhìn thấy |
| 6 | Export COCO 1.0 | `submission/labels/<mã>.json` | Ảnh không có vật vẫn có mặt |
| 7 | Validate file của mình | `python scripts/validate_labels.py submission/labels/<mã>.json` | Không báo lỗi |
| 8 | Ghi ca khó / `can_review` / `ignore_region` | tick `can_review`; `submission/qc/image_issues.csv` | Mỗi ca có ảnh, vùng, lý do |
| 9 | Ghi chú cá nhân | `submission/individual_notes/<mã>.md` | Đủ 6 mục theo mẫu |

## B. Việc riêng Người 3

Chỉ làm khi **cả nhóm đã nộp nhãn** (hết Pha 3).

### B1. Validate toàn bộ + đo IAA (Pha 4)
```bash
python scripts/validate_labels.py --all
python scripts/qc_compare.py
```
- Xong khi: lượt gán đủ `x/x`, có `submission/qc/iaa_summary.md`.

### B2. Đọc `iaa_summary.md`
- Ghi 3 số **kèm mẫu số**: IoU TB (ngưỡng ≥ 0.85), % cùng lớp (≥ 95%), số cặp box ghép.
- Ghi cặp người gán nào **CHƯA ĐẠT**.
- IoU và % cùng lớp chỉ tính trên các cặp box đã ghép. Box chưa ghép thống kê riêng.

### B3. Xem ca bất đồng bằng ảnh
```bash
python scripts/viz_disagreement.py --images flagged
```
- Mở `work/viz/`. Mỗi ca, phân loại:
  - **Cả hai cùng lệch** → guideline mơ hồ → sửa guideline.
  - **Một người lệch** → người đó chưa nắm quy tắc → sửa nhãn.
- Tìm ít nhất **1 ca cả hai giống nhau nhưng cùng sai** (IAA không bắt được).

### B4. Ghi ca cần calibration (Pha 5)
```bash
python scripts/build_final.py        # lần 1: sinh calibration_decisions.csv
```
- Điền **mỗi ca một dòng**, đủ 9 cột: `quyet_dinh`, `quy_tac_ghi_vao_guideline` (R-xx), `phien_ban_guideline` (v1.1), `nguoi_chot`, `phieu_sua`, `kiem_lai`, `pham_vi` (`anh` | `lo`).
- Phối hợp Người 2: Người 2 viết `guideline_v1.1_calibrated.md` + `submission/guideline_change.json` (`editorial` | `semantic`; `semantic` cần ≥ 1 dòng `lo`).
```bash
python scripts/prepare_calibration.py   # in ra đường dẫn labels_calibrated_<phiên-bản>.json
# sửa nhãn trên CVAT, export đúng đường dẫn đó
python scripts/build_final.py           # lần 2: labels_calibrated.json/.csv, batch_manifest.json
```

### B5. Duyệt QC (Pha 6)
```bash
python scripts/qc_sample.py --round 1
```
- Mở `work/review/round-01/`, điền `submission/qc/reviews/round-01/qc_review.csv`:
  - Ảnh sạch: `error_type=khong`, `reviewer`.
  - Lỗi box: `object_id`, `error_type` (`thua` | `sai_lop` | `sai_vi_tri_kich_thuoc` | `sai_thuoc_tinh`), `rule_id`, `note`.
  - Bỏ sót: `error_type=bo_sot`, để trống `object_id`, ghi `region`.
- Duyệt **toàn lô**. Người kiểm khác người sửa.
```bash
python scripts/qc_report.py --round 1
```

### B6. Chốt Hold / Rework / Release
| Kết quả | Khi nào | Làm tiếp |
|---|---|---|
| Hold | thiếu bằng chứng, guideline chưa chốt | ghi phần thiếu |
| Rework | > 2% ảnh lỗi hoặc lỗi lặp | thêm ca `Q01…` vào bảng quyết định → làm lại B4 → `--round 2` (giữ vòng 1) |
| Release | đạt ngưỡng, người kiểm xác nhận | viết báo cáo |

## C. Báo cáo và bàn giao (Người 3 viết, Người 1 nộp)

1. Copy `docs/QC_REPORT_TEMPLATE.md` → `submission/qc/QC_REPORT.md`. Điền đủ 10 trường bắt buộc, tỉ lệ lỗi **theo ảnh và theo đối tượng, kèm mẫu số**.
2. Điền mục "Kết quả tóm tắt" trong `TEAM.md`.
3. Kiểm:
   ```bash
   python scripts/check_submission.py --round <vòng-cuối>
   ```
   Xong khi: `0 lỗi`. Gửi Người 1 nộp.

## D. Checklist nhanh Người 3

- [ ] `validate_labels.py --all` sạch, `qc_compare.py` chạy xong
- [ ] Đọc `iaa_summary.md`, ghi số kèm mẫu số
- [ ] `viz_disagreement.py --images flagged`, phân loại ca lệch, có 1 ca "cùng sai"
- [ ] `calibration_decisions.csv`: mỗi ca một dòng, đủ 9 cột
- [ ] `labels_calibrated.json` + `batch_manifest.json`
- [ ] `qc_review.csv` đủ 40/40 ảnh, `qc_report.py` chạy xong
- [ ] Quyết định Hold / Rework / Release có lý do
- [ ] `QC_REPORT.md` + `TEAM.md` + `check_submission.py` 0 lỗi
