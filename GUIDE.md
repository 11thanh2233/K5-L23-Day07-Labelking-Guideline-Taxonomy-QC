# Hướng dẫn làm lab (từng pha)

Bài **nhóm 2–5 người**, **4 giờ**; mốc tự kiểm tra ở [CHECKPOINTS.md](CHECKPOINTS.md). Mỗi pha có **sản phẩm** phải commit. Lệnh chạy **từ thư mục gốc repo**.

```
Pha 0  Chuẩn bị               (~15')
Pha 1  Guideline cá nhân      (độc lập, ~35')
Pha 2  Thống nhất guideline   (cả nhóm, ~30')
       Nghỉ                   (10')
Pha 3  Chia việc + gán nhãn   (độc lập, ~60')
Pha 4  So sánh, đo IAA        (~20')
Pha 5  Calibration            (cả nhóm, ~40')
Pha 6  QC mẫu + báo cáo       (~30')
```

Quy tắc làm bài: [RULES.md](RULES.md). Chấm điểm: [RUBRIC.md](RUBRIC.md). Cách nộp: [SUBMISSION.md](SUBMISSION.md). Slide tham khảo: Day 07 (taxonomy, guideline, pilot, IAA, calibration, Release/Hold/Rework).
Công thức và ngưỡng: [docs/QC_CHEATSHEET.md](docs/QC_CHEATSHEET.md). Công cụ gán nhãn: [docs/CVAT_SETUP.md](docs/CVAT_SETUP.md).

## Pha 0 — Chuẩn bị (mỗi người, 15 phút)

```bash
git clone <repo public của nhóm>
cd <repo>
pip install -r requirements.txt
git config user.name  "Họ tên của bạn"
git config user.email "email gắn với tài khoản GitHub của bạn"
```

Một người fork repo thành `K4-L23-DAY07-<TenNhom>-GuidelineQC` (public), điền [TEAM.md](TEAM.md), đổi dòng tiêu đề `README.md` (xem [SUBMISSION.md](SUBMISSION.md)), mời mọi người làm collaborator.
Cách làm việc chung: **mỗi người chỉ sửa file của mình** (tên file có MSHV) nên không xung đột. Trước khi push: `git pull --rebase`.
Mỗi thành viên phải có ít nhất một commit mang tên mình.

## Pha 1 — Guideline cá nhân (độc lập, ~35 phút)

Bạn nhận [guideline/guideline_v0_starter.md](guideline/guideline_v0_starter.md). Nó **cố ý sơ sài**.

1. Mở và **xem hết 40 ảnh** trong `data/images/`. Chưa vẽ box nào.
2. Với mỗi ảnh, hỏi: *"Nếu theo đúng v0, tôi gán gì? Có chỗ nào v0 không trả lời được, hoặc hai người sẽ gán khác nhau không?"*
   Gợi ý câu hỏi để soi từng ảnh:
   - Có vật **nào trông giống** một lớp nhưng v0 không nói rõ (hay không thuộc lớp nào)?
   - Có vật **không phải vật thật** (không nên dạy mô hình coi là xe/người)?
   - Vật bị **che** hoặc bị **cắt mép**: box vẽ thế nào, thuộc tính mức mấy, ranh giới ở đâu?
   - Một người **ngồi trên xe**, một xe **chở thứ khác**: gán mấy box?
   - Vật **quá nhỏ**, **quá dày đặc**, **nhoè**, **quá tối**: gán từng vật hay không?
3. Copy v0 (hoặc dùng [guideline/TEMPLATE_guideline.md](guideline/TEMPLATE_guideline.md)) thành
   `submission/guidelines/individual/guideline_<MSHV>_<HoTen>.md` rồi **viết lại**:
   - mỗi lớp có định nghĩa, ví dụ, phản ví dụ / ca dễ nhầm;
   - thuộc tính có **mức cố định + ngưỡng đo được**;
   - quy tắc vẽ box rõ (ôm sát, che, cắt mép, phản chiếu, hình in, xe chủ…);
   - mục **Ca khó**: ghi ảnh nào (`img_0xx`), tình huống gì, bạn quyết định ra sao, vì sao;
   - câu nào bạn chưa chắc: ghi là *chưa chốt, cần họp*.
4. `git add`, commit bằng tài khoản của bạn, push.

**Sản phẩm:** `submission/guidelines/individual/guideline_<MSHV>_<HoTen>.md` của mỗi người.
Cuối bài mỗi người còn viết một ghi chú ngắn `submission/individual_notes/<MSHV>_<HoTen>.md` (mẫu: [docs/INDIVIDUAL_NOTE_TEMPLATE.md](docs/INDIVIDUAL_NOTE_TEMPLATE.md)); có thể bắt đầu điền phần Pha 1 ngay.
Đây là bản "đầu tiên" của bạn: **đừng sửa lại sau cuộc họp**; bản thống nhất viết ở file khác.

## Pha 2 — Thống nhất guideline (cả nhóm)

1. Đọc bản của nhau. Lập danh sách các chỗ **mọi người quyết khác nhau** (đó chính là chỗ guideline gốc mơ hồ).
2. Với từng chỗ: thảo luận trên ảnh, chốt **một** quyết định, ghi lý do.
3. Viết `submission/guidelines/guideline_v1.0_agreed.md` đủ **5 phần** (mục tiêu, lớp + thuộc tính, quy tắc, ca khó, QC + phiên bản).
   Cuối file có bảng lịch sử thay đổi (v0 → v1.0 đổi gì, vì ca nào).
4. Cập nhật **`submission/taxonomy.json`** cho khớp v1.0 (thêm/bớt lớp, đổi mức thuộc tính, tăng `version`).
   Chú ý phép thử: *"mô hình có phải đoán ra điều này không?"* Có → lớp. Không (chỉ để lọc, QC) → thuộc tính.
5. Sinh nhãn cho CVAT từ taxonomy mới:
   ```bash
   python scripts/make_cvat_labels.py
   ```
6. Chốt: **từ đây tới hết Pha 3 không đổi guideline.** Ca nào còn mơ hồ khi gán: tick `can_review` + ghi chú.

**Sản phẩm:** `guideline_v1.0_agreed.md`, `taxonomy.json` (đã sửa), `cvat/labels_generated.json`.

## Pha 3 — Chia việc và gán nhãn độc lập

### Chia ảnh

Mỗi ảnh phải được gán **độc lập bởi ít nhất 2 người** (nhóm 5 người: 3 người). Script chia sẵn, bạn chỉ điền danh sách MSHV:

```bash
python scripts/split_assign.py --members 22001234,22005678,22009999 --copy-images
```

- Nhóm 2–4 người: mỗi ảnh 2 người gán. Nhóm 5 người: tự động 3 người/ảnh.
- Cùng danh sách MSHV và cùng `--seed` (mặc định 42) thì cả nhóm ra **cùng một bảng chia**.
- Kết quả: `submission/qc/assignment.csv`, `submission/qc/assignments/<MSHV>.txt` (danh sách ảnh của bạn)
  và thư mục `work/<MSHV>/images/` (ảnh của bạn, đã copy; thư mục `work/` không commit).

Một người chạy lệnh, commit `submission/qc/`; những người còn lại `git pull`.

### Gán nhãn

1. Làm theo [docs/CVAT_SETUP.md](docs/CVAT_SETUP.md): tạo Project với nhãn từ `cvat/labels_generated.json`, tạo Task, upload **đúng thư mục ảnh của bạn**.
2. Gán theo **guideline v1.0 của nhóm**, **không xem nhãn của ai**, không hỏi nhau về ảnh đang làm.
3. Export **COCO 1.0** (không lưu ảnh), đặt tên `submission/labels/<MSHV>_<HoTen>.json`.
4. Kiểm trước khi commit:
   ```bash
   python scripts/validate_labels.py --all
   ```
   Sửa hết `LỖI` rồi mới push. Script chỉ kiểm lớp / thuộc tính / box trong ảnh / ảnh đủ; **không** biết box có ôm sát hay không.

**Sản phẩm:** `submission/labels/<MSHV>_<HoTen>.json` của từng thành viên, `submission/qc/assignment.csv`.

## Pha 4 — So sánh và đo IAA

Khi mọi người đã nộp nhãn:

```bash
python scripts/validate_labels.py --all
python scripts/qc_compare.py
python scripts/viz_disagreement.py --images flagged
```

Đọc `submission/qc/iaa_summary.md`:
- IoU trung bình và % cùng lớp đã đạt ngưỡng (0.85 / 95%) chưa? **Mẫu số** là gì (bao nhiêu cặp box)?
- Bao nhiêu box **không ghép được** (bỏ sót / thừa)?
- Mở `work/viz/*.png`: mỗi người một màu, nhìn thẳng chỗ lệch.

`submission/qc/calibration_candidates.csv` liệt kê từng bất thường; `flagged_images.txt` là các ảnh phải calibration.
Với mỗi nhóm bất thường, tự hỏi: **cả hai cùng lệch** (guideline mơ hồ) hay **chỉ một người lệch** (chưa nắm quy tắc)? Xem bảng cuối [docs/QC_CHEATSHEET.md](docs/QC_CHEATSHEET.md).

**Sản phẩm:** `iaa_summary.json/.md`, `calibration_candidates.csv`, `image_scores.csv`, `flagged_images.txt`, `consensus_draft.json`.

## Pha 5 — Calibration

1. **Họp:** xem lần lượt các ca trong `calibration_candidates.csv` (kèm ảnh `work/viz/`). Với mỗi ca: thảo luận, chốt một quyết định.
2. **Ghi một dòng cho mỗi quyết định.** Chạy `python scripts/build_final.py` một lần để script tạo sẵn `submission/qc/calibration_decisions.csv`, rồi điền:
   `case_id, image, quyet_dinh, quy_tac_ghi_vao_guideline, phien_ban_guideline, nguoi_chot`.
3. Quyết định nào là **quy tắc mới** thì ghi vào `submission/guidelines/guideline_v1.1_calibrated.md`
   (bản v1.0 + phần bổ sung + dòng lịch sử). Cần đổi taxonomy thì sửa `taxonomy.json` (tăng version).
   Không có quy tắc mới thì vẫn tạo file v1.1 và ghi rõ "không thay đổi quy tắc, các ca chỉ là gán nhầm".
4. **Sửa nhãn các ảnh bị cờ:**
   ```bash
   python scripts/prepare_calibration.py
   ```
   Tạo `work/calib/images/` và `work/calib/consensus_flagged.json`. Trong CVAT tạo Task mới từ các ảnh đó, nạp nhãn nháp, sửa theo quyết định,
   export COCO 1.0 thành `submission/qc/labels_calibrated_flagged.json`.
5. Gộp nhãn cuối (ảnh không lệch lấy đồng thuận, ảnh bị cờ lấy bản calibration):
   ```bash
   python scripts/build_final.py
   ```

**Sản phẩm:** `calibration_decisions.csv`, `guideline_v1.1_calibrated.md`, `labels_calibrated_flagged.json`, `labels_calibrated.json/.csv`.

## Pha 6 — QC mẫu và báo cáo

1. Lấy mẫu (mọi ảnh ca khó + 20 ảnh ngẫu nhiên) và vẽ ảnh để duyệt:
   ```bash
   python scripts/qc_sample.py --n 20 --seed 42
   ```
2. **Người kiểm nên là người ít tham gia gán ảnh đó nhất.** Mở từng ảnh trong `work/review/`, điền `submission/qc/qc_review.csv`
   (mỗi lỗi một dòng, `error_type` thuộc 5 loại; ảnh sạch ghi `khong`). Cách điền chi tiết: [scripts/README.md](scripts/README.md).
3. Tính số đo:
   ```bash
   python scripts/qc_report.py
   ```
   Thêm `--guideline-gap N` nếu còn ca guideline chưa rõ, `--data-problem N` nếu có ảnh hỏng/không dùng được (dẫn tới **Hold**).
4. Copy [docs/QC_REPORT_TEMPLATE.md](docs/QC_REPORT_TEMPLATE.md) thành `submission/qc/QC_REPORT.md`, điền theo `qc_report_auto.md`.
   Số do script chỉ là **gợi ý**: người kiểm xác nhận quyết định và giải thích.
5. Nếu quyết định là **Rework**: sửa các lỗi tìm được, cập nhật nhãn, chạy lại bước 1–3 (có thể `--force`) và ghi vòng sau vào báo cáo.
   Rework là kết quả hợp lệ; **điều bị trừ điểm là báo Release trong khi số liệu không đạt.**
6. Điền "Kết quả tóm tắt" trong `TEAM.md`, rồi:
   ```bash
   python scripts/check_submission.py
   ```
   Hết `LỖI` thì push, đối chiếu [SUBMISSION.md](SUBMISSION.md) và nộp link repo.

**Sản phẩm:** `qc_sample.csv`, `qc_review.csv`, `qc_report_auto.md`, **`QC_REPORT.md`**.

## Lỗi hay gặp

| Triệu chứng | Cách xử lý |
|---|---|
| `validate_labels` báo tên lớp lạ | CVAT còn dùng bộ nhãn cũ: tạo lại Project từ `cvat/labels_generated.json`. |
| Thiếu / thừa ảnh trong file nhãn | Task phải chứa **đúng** ảnh trong `submission/qc/assignments/<MSHV>.txt`. |
| Thuộc tính trống sau khi export | Đặt giá trị mặc định ở Project, hoặc chọn lại thuộc tính từng box. |
| Hai người cùng bất thường ở mọi ảnh | Có thể gán nhầm ảnh / nhầm Task; xem lại bước chia việc. |
| `qc_review.csv` bị báo "chưa kiểm" | Còn dòng `error_type` trống: điền `khong` hoặc loại lỗi. |
