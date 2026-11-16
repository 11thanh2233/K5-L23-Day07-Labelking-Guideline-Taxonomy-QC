# GUIDELINE GÁN NHÃN CÁ NHÂN — v0.1

**Chương trình:** VinUni AI Thực chiến K5 — Level 2 — Day 07  
**Chủ đề:** Guideline, Taxonomy & Quality Control  
**Họ tên:** Bùi Anh Dũng  
**MSSV:** 2A202603033  
**Vai trò:** Người 2 — Guideline Lead  
**Nhóm:** Labelking  
**Ngày:** 16/11/2026  
**Trạng thái:** Bản đề xuất cá nhân, chờ nhóm thống nhất

---

## 1. Mục tiêu

Xây dựng bộ dữ liệu gán nhãn đối tượng trên ảnh đường phố nhằm phục vụ huấn luyện và đánh giá mô hình Object Detection.

Các đối tượng chính bao gồm người và phương tiện giao thông.

Yêu cầu:

- Gán đúng lớp đối tượng.
- Vẽ bounding box ôm sát phần nhìn thấy.
- Gán thuộc tính nhất quán.
- Hạn chế bỏ sót đối tượng.
- Đánh dấu các trường hợp chưa chắc chắn bằng `can_review`.
- Đảm bảo dữ liệu có thể xuất từ CVAT theo định dạng COCO 1.0.

Các lỗi nghiêm trọng gồm bỏ sót người, nhầm loại phương tiện, vẽ box sai vị trí và sử dụng `ignore_region` không đúng.

## 2. Lớp và thuộc tính

### 2.1. Danh sách lớp

| Lớp | Định nghĩa | Ví dụ | Dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con, SUV, xe chở người thông thường | Sedan, hatchback, SUV | `van`, `truck` |
| `truck` | Xe tải hoặc phương tiện chuyên chở hàng hóa | Xe tải thùng, xe ben | `van` |
| `van` | Xe thùng kín cỡ nhỏ | Xe van chở hàng | `truck`, `car` |
| `motorcycle` | Xe máy và mô tô | Xe số, xe tay ga | Xe đạp |
| `person` | Người xuất hiện trong ảnh, kể cả người ngồi trên phương tiện | Người đi bộ, người lái xe | Hình người quảng cáo |
| `ignore_region` | Vùng được phép bỏ qua việc gán từng đối tượng | Đám đông không thể tách rõ | Đối tượng riêng lẻ |

**Quy tắc phân loại:**

- Một đối tượng chỉ thuộc một lớp chính.
- Không tự thêm lớp ngoài taxonomy.
- Không ép đối tượng ngoài taxonomy vào lớp gần giống.
- Nếu chưa chắc chắn, đánh dấu `can_review`.
- Không sử dụng `ignore_region` để thay thế việc gán nhãn những đối tượng có thể nhận biết rõ.

### 2.2. Thuộc tính

#### `occluded_level`

Đề xuất phân mức che khuất:

| Giá trị | Mức độ |
|---|---|
| `0` | Không bị che |
| `1` | Bị che trên 0% đến 25% |
| `2` | Bị che trên 25% đến 75% |
| `3` | Bị che trên 75% hoặc khó xác định |

Các ngưỡng phần trăm này là đề xuất cá nhân, cần nhóm xác nhận.

#### `truncated`

- `no`: Đối tượng không bị cắt bởi mép ảnh.
- `yes`: Đối tượng bị cắt bởi mép ảnh.

#### `can_review`

- Không tick: Nhãn đã được xác định tương đối chắc chắn.
- Tick: Cần reviewer kiểm tra lớp, box hoặc thuộc tính.

## 3. Quy tắc vẽ Bounding Box

### R01 — Nguyên tắc chung

Mỗi đối tượng hợp lệ được gán một bounding box riêng, ôm sát phần nhìn thấy.

### R02 — Kích thước tối thiểu

Ngưỡng hiện tại trong taxonomy là `min_box_height_px = 20`.

Đề xuất không gán đối tượng có chiều cao phần nhìn thấy dưới 20 pixel, đồng thời ghi nhận các trường hợp cần review. Cách áp dụng cuối cùng phải được nhóm xác nhận.

### R03 — Đối tượng bị che khuất

- Vẽ box quanh phần nhìn thấy.
- Không tự suy đoán phần bị che.
- Gán mức `occluded_level` phù hợp.

### R04 — Đối tượng bị cắt mép ảnh

- Vẽ box trong phạm vi ảnh.
- Gán `truncated=yes`.
- Không mở rộng box ra ngoài ảnh.

### R05 — Người ngồi trên xe máy

- Gán người bằng lớp `person`.
- Gán xe máy bằng lớp `motorcycle`.
- Cho phép hai box chồng lấn.

### R06 — Nhiều đối tượng chồng lấn

- Gán box riêng cho từng đối tượng nhận biết được.
- Không gộp nhiều người hoặc nhiều xe vào một box.
- Nếu không thể tách đối tượng, ghi nhận để nhóm quyết định có dùng `ignore_region` hay không.

### R07 — Phản chiếu và hình ảnh giả

Đề xuất không gán nhãn đối tượng chỉ xuất hiện dưới dạng hình in, quảng cáo, tượng hoặc phản chiếu.

### R08 — Ego Vehicle

Đề xuất không gán phần thân xe của chính phương tiện gắn camera nếu chỉ xuất hiện như cấu trúc tiền cảnh.

### R09 — Đối tượng ngoài taxonomy

Không tự tạo lớp mới hoặc gán sai sang lớp khác. Ghi nhận để thảo luận.

### R10 — Kiểm tra trước khi lưu

Kiểm tra class, bounding box, thuộc tính, đối tượng bỏ sót và `can_review`.

## 4. Ca khó

Các tình huống dưới đây là ví dụ đề xuất. Chưa xác nhận chúng xuất hiện trong ảnh nào của dataset.

| Ảnh | Tình huống | Rule ID | Quyết định đề xuất | Lý do |
|---|---|---|---|---|
| Chưa xác định | Người ngồi trên xe máy | R05 | Gán hai box riêng | Hai đối tượng khác lớp |
| Chưa xác định | Xe bị che một phần | R03 | Box phần nhìn thấy | Không suy đoán phần khuất |
| Chưa xác định | Xe bị cắt mép ảnh | R04 | `truncated=yes` | Phân biệt cắt ảnh và che khuất |
| Chưa xác định | Không rõ van/truck | R01, R09 | `can_review` | Cần xác nhận class |
| Chưa xác định | Người quá nhỏ | R02 | Ghi nhận review | Liên quan ngưỡng 20 px |
| Chưa xác định | Đám đông khó tách | R06 | Xem xét `ignore_region` | Không thể gán riêng đáng tin cậy |
| Chưa xác định | Hình người quảng cáo | R07 | Không gán | Không phải người thật |

Sau khi quan sát 40 ảnh, cần thay các ô "Chưa xác định" bằng mã ảnh thực tế và ghi nhận quyết định đã được xác minh.

## 5. QC và phiên bản

### 5.1. Ngưỡng QC

Các giá trị lấy từ `submission/taxonomy.json` v0:

| Chỉ số | Giá trị |
|---|---:|
| `min_box_height_px` | 20 |
| `iou_thr_large` | 0.85 |
| `iou_thr_small` | 0.70 |
| `large_px` | 50 |
| `iaa_iou` | 0.85 |
| `iaa_class` | 0.95 |
| `error_rate_img_max` | 0.02 |
| `match_iou` | 0.50 |

Cách tính và áp dụng các chỉ số tuân theo script của repository.

### 5.2. Quy trình QC

1. Annotator tự kiểm tra nhãn.
2. Xuất dữ liệu COCO 1.0.
3. Chạy script validation.
4. So sánh nhãn độc lập giữa các thành viên.
5. Tổng hợp các trường hợp bất đồng.
6. Thảo luận calibration.
7. Cập nhật guideline nếu có thay đổi quy tắc.
8. Kiểm tra lại dữ liệu theo guideline đã thống nhất.

### 5.3. Phân công trách nhiệm

- **Annotator:** Gán nhãn và ghi nhận ca khó.
- **Guideline Lead:** Tổng hợp quy tắc và taxonomy.
- **QC Lead:** Phân tích bất đồng và kiểm tra chất lượng.
- **Team Lead:** Điều phối và tổ chức phê duyệt kết quả cuối cùng.

### 5.4. Lịch sử phiên bản

| Phiên bản | Thay đổi | Trạng thái |
|---|---|---|
| v0 | Guideline ban đầu của giảng viên | Tài liệu gốc |
| v0.1 | Bổ sung lớp, thuộc tính, quy tắc và ca khó | Đề xuất cá nhân |
| v1.0 | Guideline thống nhất của nhóm | Chưa chốt |
| v1.1 | Điều chỉnh sau calibration | Chưa thực hiện |

---

**Kết luận:** Guideline v0.1 này là bản đề xuất cá nhân của Bùi Anh Dũng. Các quy tắc mới cần được nhóm Labelking thống nhất trước khi sử dụng làm guideline chính thức cho việc gán nhãn và đánh giá chất lượng.
