# Day 07 Lab — Nhóm <TÊN NHÓM>: <MSHV1> - <Họ và tên 1>, <MSHV2> - <Họ và tên 2>

> **BƯỚC ĐẦU TIÊN:** sửa dòng tiêu đề ở trên thành danh sách thật, ví dụ
> `# Day 07 Lab — Nhóm Alpha: 22001234 - Nguyễn Văn A, 22005678 - Trần Thị B, 22009999 - Lê Văn C`
> (đủ **mọi** thành viên, đúng dạng `MSHV - Họ và tên`). Xong thì xoá khung trích dẫn này.

**Lab Day 07: Guideline, Taxonomy và quy trình QC.** Cả nhóm nhận một guideline sơ sài (v0) và 40 ảnh đường phố
chứa nhiều tình huống mà v0 không nói tới. Việc của nhóm là **viết lại guideline cho đủ dùng**, chia việc, gán nhãn độc lập,
đo độ đồng thuận, họp calibration, rồi ra quyết định Release / Hold / Rework cho lô nhãn.

> Trọng tâm của bài là **guideline**: nhãn chỉ tốt khi mọi người hiểu quy tắc giống nhau.

## Bắt đầu

1. Một người **fork** repo này thành **repo public** của nhóm; mời các bạn còn lại làm collaborator
   (Settings → Collaborators). Mỗi người `git clone` về máy.
2. Đọc **[GUIDE.md](GUIDE.md)** (các pha làm việc, lệnh, thời lượng) và **[RULES.md](RULES.md)**.
3. Đặt tên repo theo [SUBMISSION.md](SUBMISSION.md), điền [TEAM.md](TEAM.md).
4. Python 3.9+ và `pip install -r requirements.txt`.

## Tài liệu hướng dẫn

| Bạn cần tìm | Tài liệu |
|---|---|
| Các pha làm việc, lệnh chạy | [GUIDE.md](GUIDE.md) |
| Mốc tiến độ trong 4 giờ | [CHECKPOINTS.md](CHECKPOINTS.md) |
| Quy tắc (độc lập, AI, số liệu trung thực) | [RULES.md](RULES.md) |
| Tiêu chí chấm điểm (100 điểm) | [RUBRIC.md](RUBRIC.md) |
| Cách nộp, tên repo, checklist | [SUBMISSION.md](SUBMISSION.md) |
| Thông tin nhóm | [TEAM.md](TEAM.md) |
| Dùng CVAT | [docs/CVAT_SETUP.md](docs/CVAT_SETUP.md) |
| Công thức, ngưỡng, cây quyết định QC | [docs/QC_CHEATSHEET.md](docs/QC_CHEATSHEET.md) |
| Mẫu báo cáo QC, ghi chú cá nhân | [docs/QC_REPORT_TEMPLATE.md](docs/QC_REPORT_TEMPLATE.md), [docs/INDIVIDUAL_NOTE_TEMPLATE.md](docs/INDIVIDUAL_NOTE_TEMPLATE.md) |
| Chi tiết các script | [scripts/README.md](scripts/README.md) |

## Quy tắc nộp bài

- Repo **public**, có **commit của mọi thành viên** (mỗi người commit file của chính mình bằng tài khoản Git của mình).
- Tiêu đề README (dòng đầu) liệt kê **MSHV - Họ và tên** của mọi thành viên.
- Làm **độc lập** ở Pha 1 và Pha 3: không xem guideline/nhãn của nhau trước khi tới bước họp.
- Mỗi thành viên có ghi chú cá nhân `submission/individual_notes/<MSHV>_<HoTen>.md`.
- Trước khi nộp chạy `python scripts/check_submission.py` cho tới khi hết lỗi.

## Sản phẩm phải có trong repo

| # | Sản phẩm | Vị trí |
|---|---|---|
| 1 | Guideline **đầu tiên của từng thành viên** (bản v0 do mỗi người tự sửa) | `submission/guidelines/individual/guideline_<MSHV>_<HoTen>.md` |
| 2 | Guideline **sau khi cả nhóm thống nhất** | `submission/guidelines/guideline_v1.0_agreed.md` |
| 3 | Guideline sau calibration (nếu có quy tắc mới) | `submission/guidelines/guideline_v1.1_calibrated.md` |
| 4 | Taxonomy của nhóm (lớp, thuộc tính) | `submission/taxonomy.json` |
| 5 | Bảng chia việc | `submission/qc/assignment.csv` |
| 6 | Nhãn **của từng thành viên** (COCO 1.0 từ CVAT) | `submission/labels/<MSHV>_<HoTen>.json` |
| 7 | CSV các ảnh / nhãn **cần calibration** | `submission/qc/calibration_candidates.csv` (+ `flagged_images.txt`) |
| 8 | Quyết định calibration, **mỗi quyết định một dòng** | `submission/qc/calibration_decisions.csv` |
| 9 | Tập nhãn **sau calibration** | `submission/qc/labels_calibrated.json` (+ `.csv`) |
| 10 | Mẫu QC và phiếu kiểm | `submission/qc/qc_sample.csv`, `submission/qc/qc_review.csv` |
| 11 | **Báo cáo QC** | `submission/qc/QC_REPORT.md` |
| 12 | Ghi chú cá nhân của từng thành viên | `submission/individual_notes/<MSHV>_<HoTen>.md` |
| 13 | Thông tin nhóm | `TEAM.md` |

Quy ước tên: `<MSHV>` là mã số học viên (chữ số), `<HoTen>` là họ tên không dấu, viết liền, ví dụ `22001234_NguyenVanA`.

## Tiến độ của nhóm (điền khi làm)

| Pha | Việc | Xong? |
|---|---|---|
| 1 | Mỗi người đọc 40 ảnh, sửa guideline cá nhân | ☐ |
| 2 | Họp nhóm, thống nhất `guideline_v1.0_agreed.md`, cập nhật `taxonomy.json` | ☐ |
| 3 | Chia ảnh, gán độc lập, nộp nhãn từng người | ☐ |
| 4 | So sánh, đo IAA, lấy ca bất thường | ☐ |
| 5 | Calibration: chốt quy tắc, sửa nhãn, gộp nhãn cuối | ☐ |
| 6 | Lấy mẫu QC, kiểm, viết báo cáo, quyết định | ☐ |

## Kết quả tóm tắt (điền cuối bài)

- Số thành viên / số lần gán mỗi ảnh (K): …
- IAA trước calibration: IoU trung bình … , đồng thuận lớp … %
- Số ảnh phải calibration: … / 40
- Tỉ lệ lỗi sau calibration: … % theo ảnh (…/…), … % theo đối tượng (…/…)
- **Quyết định:** Release / Hold / Rework — lý do một dòng: …

## Nguồn ảnh

40 ảnh lấy từ Wikimedia Commons theo giấy phép mở, đã thu nhỏ. Tác giả, giấy phép và liên kết từng ảnh nằm ở
[data/ATTRIBUTION.csv](data/ATTRIBUTION.csv) (xem [data/README.md](data/README.md)).
