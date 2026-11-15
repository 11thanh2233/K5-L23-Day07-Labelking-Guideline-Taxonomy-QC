# CVAT: cài đặt và dùng cho lab

Dùng **cvat.ai** (bản cloud, tài khoản miễn phí) hoặc CVAT tự cài của lớp. Học viên đã dùng CVAT ở Day 02–05.

## 1. Tạo Project với nhãn của nhóm

1. **Projects → Create new project**, đặt tên `day07-<MSHV>`.
2. Mục **Labels → Raw**: dán toàn bộ nội dung `cvat/labels_generated.json` (sinh bằng `python scripts/make_cvat_labels.py`
   sau khi nhóm sửa `submission/taxonomy.json`). Bấm **Done**, rồi **Submit & Open**.
3. Kiểm tra: mỗi lớp có đủ thuộc tính `occluded_level`, `truncated`, `can_review` (riêng `ignore_region` không cần thuộc tính).

Nhãn trong CVAT **phải trùng tên** với `taxonomy.json`; script so khớp theo tên lớp.

## 2. Tạo Task với đúng ảnh của bạn

1. **Create new task**, chọn Project ở bước 1.
2. Upload **tất cả ảnh trong `work/<MSHV>/images/`** (kéo thả thư mục hoặc chọn nhiều file). Không upload ảnh ngoài danh sách.
3. Đếm: số ảnh trong Task phải bằng số dòng trong `submission/qc/assignments/<MSHV>.txt`.

## 3. Gán box

| Phím | Việc |
|---|---|
| `N` | vẽ box (lần đầu chọn **Rectangle**, đúng lớp) |
| `Ctrl` + `1…9`, `0` | đổi lớp của box đang chọn |
| `F` / `D` | ảnh sau / ảnh trước |
| `Ctrl` + `S` | lưu (lưu thường xuyên) |

- Bấm hai góc đối diện: box tự đóng. Chọn thuộc tính ở thẻ đối tượng (panel phải, mục Objects).
- Cờ `occluded` có sẵn của CVAT (phím `Q`) **khác** `occluded_level` của nhóm: script bỏ qua cờ `Q`, chỉ đọc `occluded_level`.
- Vùng bỏ qua: vẽ Rectangle lớp `ignore_region`.
- Ca mơ hồ: mở thẻ đối tượng, tick `can_review`, ghi chú nơi quy ước (ví dụ tên file / mô tả trong chat nhóm **sau khi** nộp nhãn).
- Ảnh không có vật nào cần gán: để trống, vẫn tính là đã gán.

## 4. Export nhãn

1. Menu **Actions → Export task dataset**.
2. **Format: COCO 1.0**, **Save images: tắt**, OK.
3. Tải file `.zip` từ trang **Requests**, giải nén: lấy `annotations/instances_default.json`.
4. Đổi tên thành `submission/labels/<MSHV>_<HoTen>.json`.
5. `python scripts/validate_labels.py --all` rồi commit.

Bản gán nên ghi kèm phiên bản guideline (v1.0) trong tin nhắn commit.

## 5. Task calibration (Pha 5)

1. `python scripts/prepare_calibration.py` → `work/calib/images/` + `work/calib/consensus_flagged.json`.
2. Tạo Task mới (cùng Project) từ các ảnh trong `work/calib/images/`.
3. **Actions → Upload annotations → COCO 1.0** → chọn `work/calib/consensus_flagged.json`.
4. Sửa theo quyết định calibration. Nếu CVAT không nạp thuộc tính, chọn lại bằng tay.
5. Export COCO 1.0 → `submission/qc/labels_calibrated_flagged.json`.

Nếu việc nạp nhãn nháp lỗi, gán lại các ảnh đó từ đầu (xem ảnh chồng nhãn trong `work/viz/` làm tham chiếu).

## Gỡ rối

- **Không thấy thuộc tính trong JSON export:** ở Project đặt `default_value`; mở một box, chọn thuộc tính, lưu rồi export lại.
- **Tên file trong JSON có tiền tố `images/`:** bình thường, script bỏ tiền tố.
- **Export báo lỗi:** đợi vài giây rồi tải lại ở trang Requests.
