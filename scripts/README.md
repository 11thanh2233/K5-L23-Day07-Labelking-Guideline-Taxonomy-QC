# Scripts của lab

Chạy **từ thư mục gốc của repo** (`python scripts/<tên>.py`). Cần Python 3.9+ và `pip install -r requirements.txt` (chỉ cần Pillow, cho phần vẽ ảnh). Mọi script đều có `--help`.

Các script đọc lớp/thuộc tính/ngưỡng từ `submission/taxonomy.json` - khi nhóm đổi taxonomy, **chỉ sửa file đó** (và `version`), không sửa code.

## Thứ tự chạy

| # | Pha | Lệnh | Việc làm | Đầu ra |
|---|---|---|---|---|
| 1 | Chuẩn bị CVAT | `python scripts/make_cvat_labels.py` | Sinh JSON để dán vào CVAT (Project → Labels → Raw) | `cvat/labels_generated.json` |
| 2 | Chia ảnh | `python scripts/split_assign.py --members 123,456,789 --copy-images` | Mỗi ảnh K người gán độc lập (K=2; nhóm 5 người → K=3) | `submission/qc/assignment.csv`, `submission/qc/assignments/<MSHV>.txt`, `work/<MSHV>/images/` |
| 3 | Gán nhãn | (CVAT) | Gán đúng ảnh của mình, **không xem nhãn người khác**; export *COCO 1.0* | `submission/labels/<MSHV>_<HoTen>.json` |
| 4 | Kiểm trước khi nộp | `python scripts/validate_labels.py --all` | Kiểm tên file, lớp, thuộc tính, box trong ảnh, ảnh đủ/thừa | (in màn hình; exit 1 nếu lỗi) |
| 5 | So sánh / IAA | `python scripts/qc_compare.py` | Đo IAA, tìm ca bất thường, dựng đồng thuận nháp | `submission/qc/` (xem bảng dưới) |
| 6 | Xem ca lệch | `python scripts/viz_disagreement.py --images flagged` | Vẽ chồng box từng người | `work/viz/*.png`, `work/viz/_overview.png` |
| 6b | Gói calibration | `python scripts/prepare_calibration.py` | Copy các ảnh bị cờ + nhãn đồng thuận nháp của riêng chúng để nạp vào CVAT | `work/calib/images/`, `work/calib/consensus_flagged.json` |
| 7 | Calibration | (họp nhóm + CVAT) | Chốt quy tắc, mỗi quyết định **một dòng**, sửa lại ảnh bị cờ, export COCO | `calibration_decisions.csv`, `labels_calibrated_flagged.json` |
| 8 | Gộp nhãn cuối | `python scripts/build_final.py` | Ảnh không lệch lấy đồng thuận, ảnh bị cờ lấy bản calibration | `labels_calibrated.json`, `labels_calibrated.csv` |
| 9 | Lấy mẫu QC | `python scripts/qc_sample.py --n 20 --seed 42` | Mẫu = mọi ca khó + n ảnh ngẫu nhiên; tạo phiếu kiểm | `qc_sample.csv`, `qc_review.csv`, `work/review/*.png` |
| 10 | Số liệu QC | `python scripts/qc_report.py` | Tính tỉ lệ lỗi, top lỗi, **gợi ý** Hold/Rework/Release | `qc_report_auto.md` |

`python scripts/viz_disagreement.py` cũng nhận: `--images all`, `--images img_003.jpg img_010.jpg`, `--source consensus|final`.

## Đầu ra của `qc_compare.py` (trong `submission/qc/`)

| File | Ý nghĩa |
|---|---|
| `iaa_summary.json` / `.md` | IoU trung bình, % cùng lớp, % cùng thuộc tính, số box chưa ghép; theo từng cặp người và tổng; đạt/chưa đạt ngưỡng. IoU và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU ≥ `match_iou`); box không ghép được thống kê riêng. |
| `calibration_candidates.csv` | Mỗi dòng một ca bất thường (cần mang ra họp calibration) |
| `image_scores.csv` | Mỗi ảnh: số người gán, số bất thường, điểm (bỏ sót/sai lớp nặng 2, còn lại 1), cờ cần calibration |
| `consensus_draft.json` | COCO đồng thuận **nháp** cho mọi ảnh (lớp/thuộc tính theo đa số, box = trung bình toạ độ). Box còn tranh cãi có `needs_calibration=true` |
| `flagged_images.txt` | Danh sách ảnh có ≥ 1 bất thường (kể cả cờ `can_review`) → phải calibration |

Cột `calibration_candidates.csv`: `case_id` (C001…), `image`, `issue_type` (`bo_sot_thua` / `sai_lop` / `iou_thap` / `sai_thuoc_tinh` / `co_can_review`), `annotators` (cặp `A|B`), `class_a`, `class_b`, `box_a`, `box_b` (dạng `[x,y,w,h]`), `iou`, `ghi_chu_tu_dong`.
Nếu nhóm ≥ 3 người, một bất đồng có thể xuất hiện ở nhiều cặp (mỗi cặp một dòng).

Quy ước so sánh: ghép box 1-1 theo IoU giảm dần, không phân biệt lớp, ngưỡng `match_iou` (0.5). Box chưa ghép mà ≥ 50% diện tích nằm trong `ignore_region` thì **không** tính là lỗi. Ngưỡng IoU từng box: cao ≥ 50 px → 0.85, nhỏ hơn → 0.7. Ngưỡng IAA: IoU TB ≥ 0.85 và đồng thuận lớp ≥ 95%.

## File học viên tự điền

**`submission/qc/calibration_decisions.csv`** (script tạo file mẫu lần đầu chạy `build_final.py`):
`case_id, image, quyet_dinh, quy_tac_ghi_vao_guideline, phien_ban_guideline, nguoi_chot`. Mỗi quyết định ghi **một dòng**; mỗi ảnh bị cờ cần ≥ 1 dòng có `quyet_dinh`.

**`submission/qc/labels_calibrated_flagged.json`**: COCO 1.0 export từ CVAT của các ảnh bị cờ sau khi sửa theo quyết định (cùng taxonomy).

**`submission/qc/qc_review.csv`** (phiếu kiểm, script tạo sẵn một dòng/ảnh mẫu): `image, object_id, error_type, reviewer, note`.
- Mở ảnh trong `work/review/` (id từng vật in sẵn, ví dụ `#12 car`).
- Ảnh không lỗi: điền `error_type = khong` (đổi dòng của ảnh đó).
- Ảnh có lỗi: **mỗi lỗi một dòng** (thêm dòng nếu cần); `object_id` là id trên ảnh; lỗi bỏ sót không có id thì để trống và mô tả trong `note`.
- `error_type` chỉ nhận: `khong`, `bo_sot`, `thua`, `sai_lop`, `sai_vi_tri_kich_thuoc`, `sai_thuoc_tinh`.
- Ảnh còn trống `error_type` bị coi là **chưa kiểm**; script cảnh báo.
- Script không ghi đè file này khi đã tồn tại (chỉ khi `--force`).

## `qc_report.py`

Tỉ lệ lỗi báo **cả hai cách và ghi rõ mẫu số**: theo đối tượng (lỗi/đối tượng trong mẫu) và theo ảnh (ảnh có lỗi/ảnh trong mẫu). Ngưỡng Release (`error_rate_img_max`, 2%) áp dụng cho tỉ lệ **theo ảnh**. Cây quyết định gợi ý: Hold (`--guideline-gap N` hoặc `--data-problem N` > 0) → Rework (ảnh lỗi > ngưỡng, hoặc một loại lỗi chiếm ≥ 50% và ≥ 3 lỗi, hoặc IAA dưới ngưỡng) → Release. `QC_REPORT.md` do nhóm tự viết; script không bao giờ ghi file đó.

## Script kiểm được gì, không kiểm được gì

Kiểm được: tên file, lớp có trong taxonomy, giá trị thuộc tính hợp lệ, box nằm trong ảnh, box quá nhỏ, đủ ảnh được giao, độ lệch giữa người gán (IoU, lớp, thuộc tính, bỏ sót/thừa), các số đo QC.

**Không** kiểm được: box có ôm sát vật thật hay không, lớp có đúng thực tế không, có bỏ sót vật mà **cả nhóm cùng bỏ sót** không, hay mọi người **cùng hiểu sai** quy tắc. Những việc đó cần mắt người đối chiếu với guideline/ảnh gốc.

## Lưu ý định dạng CVAT

Script map lớp theo **tên** (id danh mục khác nhau giữa các file) và ảnh theo **tên file** (bỏ tiền tố thư mục). Thuộc tính `occluded_level` / `truncated` / `can_review` được chuẩn hoá (chuỗi thường, `true/false` ↔ `yes/no`). Cờ `occluded` có sẵn của CVAT bị bỏ qua. Ảnh có trong `images` nhưng không có annotation được hiểu là "đã gán, không có vật".

## Tự kiểm bài nộp

`python scripts/check_submission.py` kiểm tiêu đề README (đủ `MSHV - Họ tên`), guideline cá nhân từng người, guideline thống nhất, nhãn từng người, các file CSV/JSON và báo cáo QC, số tác giả commit. Chỉ kiểm có/đủ, không chấm nội dung.
