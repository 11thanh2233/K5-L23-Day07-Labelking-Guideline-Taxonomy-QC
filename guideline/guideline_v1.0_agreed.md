# GUIDELINE GÁN NHÃN — LABELKING — v1.0 (BẢN HOÀN THIỆN ĐỀ XUẤT)

> **Trạng thái:** Bản biên tập và bổ sung để nhóm xác nhận, **chưa thay thế** `submission/guidelines/guideline_v1.0_agreed.md` đang được nhóm chốt. Các nội dung đánh dấu **[CẦN NHÓM XÁC NHẬN]** có thể ảnh hưởng quyết định gán nhãn và phải được thống nhất trước khi áp dụng.

- **Chương trình:** VinUni AI Thực chiến K5 — Level 2 — Day 07
- **Nhóm:** Labelking
- **Phiên bản nền:** `guideline_v1.0_agreed.md` ngày 16/11/2026
- **Người biên tập bản đề xuất:** Guideline Lead (mã thành viên 102)
- **Công cụ:** CVAT Local; xuất COCO 1.0
- **Phạm vi:** Ảnh đường phố 2D; gán bounding box cho người và phương tiện

## 0. Nguyên tắc thống nhất và thứ tự ưu tiên

1. **Một vật thật, đủ nhận diện → một bounding box**, đúng lớp; không gộp người và xe máy thành một vật.
2. **Box chỉ ôm sát phần nhìn thấy**, không suy đoán phần ẩn hay kéo ra ngoài ảnh.
3. **Không tạo lớp mới.** Vật không thuộc 5 lớp đối tượng thì không gán thành đối tượng hợp lệ.
4. **`ignore_region` là vùng bỏ qua, không phải lớp đối tượng thật.** Chỉ dùng cho vùng thực sự cần loại trừ khỏi đánh giá/gán nhãn theo quyết định chung.
5. **Không chắc → `can_review=true` khi đã có box đủ căn cứ;** nếu chưa thể vẽ box có căn cứ, ghi vấn đề ở mức ảnh cho QC.
6. Mọi annotator dùng cùng phiên bản guideline và taxonomy; không tự thay đổi quy tắc giữa lượt gán độc lập.

### Mã quy tắc chuẩn

| Rule ID | Nội dung |
|---|---|
| **R-01** | Box ôm sát phần nhìn thấy |
| **R-02** | Người và xe máy là hai vật riêng |
| **R-03** | Xe chở xe và xe trên thùng |
| **R-04** | Vật bị che khuất và cắt mép ảnh |
| **R-05** | Vật quá nhỏ / vật không phải vật thật |
| **R-06** | Đám đông / vùng dày đặc |
| **R-07** | `can_review` và chuyển ca mơ hồ cho reviewer |

> **Sửa lỗi biên tập:** Phần “Bản chốt” của tài liệu gốc từng dùng `R-01` cho người–xe máy và `R-02` cho xe chở xe, trong khi các phần còn lại dùng mã khác. Bảng trên thống nhất theo mục 3 và mục 6 của guideline gốc.

## 1. Mục tiêu và phạm vi

Tạo dữ liệu gán nhãn nhất quán để huấn luyện và đánh giá mô hình phát hiện người và phương tiện trong ảnh đường phố tại Việt Nam. Ưu tiên tránh sai lớp, thiếu hoặc gộp box, suy đoán phần bị che và gán nhầm phản xạ/đồ chơi/hình in thành vật thật.

- **Đơn vị nhãn:** bounding box hình chữ nhật, một box cho một đối tượng hợp lệ.
- **Đối tượng:** `car`, `truck`, `van`, `motorcycle`, `person`.
- **Vùng đặc biệt:** `ignore_region`.
- **Ngoài phạm vi:** đối tượng không thuộc các lớp trên; không tự thêm lớp `bus`, `bicycle`, `traffic_light` hoặc các lớp khác.

## 2. Taxonomy — lớp và thuộc tính

### 2.1. Các lớp

| Lớp | Định nghĩa thao tác | Ví dụ | Không gán nhầm thành |
|---|---|---|---|
| `car` | Ô tô con, xe du lịch, sedan, hatchback, SUV, taxi có hình thái ô tô con rõ | Sedan, SUV, taxi | `truck` là xe chở hàng/chở xe; `van` là xe thùng kín cỡ nhỏ |
| `truck` | Xe tải, xe chở hàng, xe chở xe, phương tiện có kết cấu phục vụ vận tải hàng/xe | Xe tải thùng, xe chở ô tô | `car` chỉ vì cabin trông như xe con; `van` cỡ nhỏ |
| `van` | Xe thùng kín cỡ nhỏ, phục vụ chở hàng hoặc vận chuyển nhỏ | Van chở hàng, xe thùng mini | `truck` tải lớn; `car` có kiểu thân xe du lịch |
| `motorcycle` | Xe máy, mô tô, phương tiện hai bánh thuộc phạm vi nhóm đã thống nhất | Xe máy, mô tô | `person` là người lái/ngồi trên xe |
| `person` | Người đi bộ hoặc trên phương tiện, khi phần người còn đủ rõ để nhận diện | Người đi bộ, người ngồi xe máy | Xe máy, hình in người, tượng/manơcanh |
| `ignore_region` | **Vùng bỏ qua**, không đại diện một vật; dùng khi không thể hoặc không cần tách nhãn từng đối tượng trong vùng theo quy tắc nhóm | Đám đông không tách được; vùng phản xạ/hình in gây nhiễu nếu nhóm quyết định loại trừ | Một người hoặc phương tiện thật, rõ ràng và tách được |

**[CẦN NHÓM XÁC NHẬN]** Khi khó phân biệt `car`/`van`/`truck`, ưu tiên cấu trúc thân xe và chức năng nhìn thấy được (thùng hàng, cabin, xe chở xe), **không dùng kích thước pixel đơn thuần** vì phối cảnh làm thay đổi kích thước biểu kiến. Nếu vẫn không chắc, đánh dấu `can_review` thay vì tự áp đặt một ngưỡng kích thước xe.

### 2.2. Thuộc tính

| Thuộc tính | Giá trị | Quy tắc |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Phân loại theo tỷ lệ **ước lượng phần đối tượng nhìn thấy**, không phải tỷ lệ phần bị che; xem bảng dưới |
| `truncated` | `no`, `yes` | `yes` khi đối tượng bị **mép ảnh** cắt; không đồng nhất với bị vật khác che |
| `can_review` | `false`, `true` | `true` khi cần reviewer xác nhận lớp, box, thuộc tính hoặc số đối tượng; mặc định `false` |

**Cách đọc ngưỡng `occluded_level` theo ý nghĩa từ guideline gốc:**

| Mức | Phần đối tượng ước lượng còn nhìn thấy | Diễn giải |
|---|---|---|
| `0` | Trên 80% | Rõ hoặc che rất ít |
| `1` | Trên 50% đến 80% | Che nhẹ |
| `2` | Từ 20% đến 50% | Che nhiều |
| `3` | Dưới 20% | Che cực nhiều; chỉ gán nếu vẫn nhận diện được |

**[CẦN NHÓM XÁC NHẬN]** Quy ước biên chính xác 20%, 50%, 80% như bảng trên là cách diễn giải để tránh trùng khoảng; guideline gốc chưa chỉ rõ cách xử lý tại đúng điểm biên. Nếu tỷ lệ chỉ ước lượng được, annotator ghi `can_review=true` cho ca sát ngưỡng.

**Phân biệt che khuất và cắt mép:** Nếu xe bị cây che và đồng thời bị cắt ở mép ảnh, đặt `occluded_level` theo phần bị che bởi cây và `truncated=yes` do mép ảnh. Không dùng `truncated=yes` chỉ vì có vật khác che.

## 3. Quy tắc vẽ bounding box

### R-01 — Chỉ ôm sát phần nhìn thấy

- Mỗi vật thật và đủ rõ có một box riêng; box bám sát các điểm cực trị của **phần vật đang nhìn thấy**.
- Không mở rộng để bao phần nằm sau vật cản hoặc ngoài khung ảnh.
- Không gộp hai vật chỉ vì chúng chồng lên nhau.
- Box phải nằm trong giới hạn ảnh; không vẽ box có chiều rộng/chiều cao bằng 0.

### R-02 — Người và xe máy

- Khi người lái/ngồi trên xe và xe máy đều nhận diện được: **hai box** `person` và `motorcycle`.
- Khi chỉ thấy xe máy rõ còn người quá khuất/không thể xác nhận: chỉ gán `motorcycle`.
- Khi chỉ thấy người đủ rõ nhưng xe không đủ nhận diện: chỉ gán `person`.
- Không vẽ một box bao cả người và xe rồi gán `motorcycle`.

### R-03 — Xe chở xe

- Xe chuyên chở ô tô: box `truck` cho phương tiện chở xe.
- Mỗi ô tô trên thùng được gán box `car` riêng **nếu nhìn rõ và tách được**.
- Không gộp toàn bộ ô tô trên thùng với xe chở thành một nhãn duy nhất.
- Nếu không thể tách từng xe một cách có căn cứ, ghi ca cần review; không đoán số xe.

### R-04 — Che khuất và cắt mép

- Vật bị che: chỉ vẽ phần thấy được; chọn `occluded_level` theo mục 2.2.
- Vật bị cắt ở mép ảnh: box dừng ở mép; `truncated=yes`.
- Có thể đồng thời có che khuất và cắt mép.
- Nếu vật không đủ bằng chứng để nhận diện, không dựng box từ phần ẩn tưởng tượng.

### R-05 — Vật quá nhỏ, phản xạ, hình in, đồ chơi

- Không gán phản xạ trên kính, hình in trên biển quảng cáo, tượng/manơcanh, mô hình hoặc đồ chơi như vật thật.
- Theo taxonomy gốc, `min_box_height_px = 20` là ngưỡng quy tắc cần tuân thủ; **[CẦN NHÓM XÁC NHẬN]** cách áp dụng: đối tượng có box cao **dưới 20 px** thì không gán box đối tượng; trường hợp bằng 20 px được xét nếu đủ rõ. Nếu nhóm muốn ngoại lệ, phải ghi rõ trong guideline và đối chiếu validator.
- Không mặc định vẽ `ignore_region` cho từng vật nhỏ/đồ chơi/phản xạ. **[CẦN NHÓM XÁC NHẬN]** chỉ vẽ ignore khi có một **vùng** cần loại trừ rõ ràng và được nhóm chấp thuận; nếu không, bỏ qua vật ngoài phạm vi.

### R-06 — Đám đông và vùng dày đặc

- Nếu từng người/xe còn phân biệt rõ: vẽ box riêng từng vật.
- Nếu một vùng quá dày, không thể xác định số vật hoặc ranh giới đáng tin cậy: đề xuất dùng `ignore_region` cho vùng đó sau khi nhóm thống nhất.
- Không dùng một box `person` để bao cả đám đông.
- Không đặt ignore đè lên đối tượng rõ ràng có thể gán riêng mà không có lý do QC.

### R-07 — Đánh dấu cần review

- Khi đã đủ bằng chứng để tạo box nhưng còn mơ hồ về lớp, số box, vị trí hoặc mức che: gán theo phương án có căn cứ nhất và đặt `can_review=true`.
- Khi **không đủ bằng chứng để vẽ box**, không tạo box giả; ghi ca vào bảng vấn đề ảnh (`image,annotator,region,note`) theo quy trình sau khi khóa nhãn.
- Reviewer ghi quyết định và Rule ID; không dùng `can_review` thay cho việc tự kiểm tra.

## 4. Ca khó của bộ ảnh Day 07

| Ảnh | Tình huống ghi trong guideline nhóm | Rule ID chuẩn | Quyết định gán nhãn | Lưu ý QC |
|---|---|---|---|---|
| `img_002` | Xe chở nhiều ô tô | R-03 | `truck` cho xe chở xe; từng `car` rõ và tách được có box riêng | Kiểm tra gộp box, bỏ sót xe |
| `img_005` | Người trên xe máy, cả hai rõ | R-02 | Hai box `person` và `motorcycle` | Không gộp người và xe |
| `img_013` | Người đi xe máy bị che hoặc khó nhận diện | R-02, R-04, R-07 | Chỉ gán vật đủ nhận diện; box ôm phần thấy; ca mơ hồ cần review | Không suy đoán phần khuất |
| `img_036` | Mô hình, đồ chơi hoặc vật rất nhỏ | R-05 | Không gán như vật thật | Xác minh khi nào cần vùng ignore |
| `img_025`, `img_038` | Nhiều người, vật nhỏ hoặc che nặng | R-06, R-07 | Gán từng vật đủ rõ; vùng không tách được cần quyết định ignore/review | Tránh gộp đám đông |

> Các mô tả trên kế thừa quyết định từ guideline nhóm, **không phải kết luận mới từ việc quan sát trực tiếp từng ảnh**. Nếu ảnh thực tế cho thấy chi tiết khác, cần đưa vào nhật ký QC để nhóm xác nhận.

## 5. QC và ngưỡng cố định

Các giá trị dưới đây **giữ nguyên** từ `submission/taxonomy.json` v0 theo yêu cầu của bài lab:

| Khóa trong `rules` | Giá trị |
|---|---:|
| `min_box_height_px` | 20 |
| `iou_thr_large` | 0.85 |
| `iou_thr_small` | 0.70 |
| `large_px` | 50 |
| `iaa_iou` | 0.85 |
| `iaa_class` | 0.95 |
| `error_rate_img_max` | 0.02 |
| `match_iou` | 0.50 |

Không tự chỉnh các ngưỡng này để đạt điểm QC. Phải kiểm tra đầy đủ số ảnh theo phân công; ảnh không có vật vẫn phải xuất hiện trong COCO.

### Checklist tự kiểm trước khi lưu CVAT

- [ ] Chỉ dùng đúng 6 lớp trong taxonomy; không thêm lớp mới.
- [ ] Mỗi người và xe máy đủ rõ có box riêng.
- [ ] Box ôm sát phần nhìn thấy; không kéo ra phần ẩn hoặc ngoài mép ảnh.
- [ ] `occluded_level` và `truncated` được đặt độc lập, đúng ngữ nghĩa.
- [ ] Không gán phản xạ, đồ chơi, hình in thành người/xe thật.
- [ ] Vật nhỏ, vùng dày đặc và `ignore_region` được xử lý theo quyết định nhóm.
- [ ] Các box chưa chắc có `can_review=true`; ca không thể vẽ được ghi vào nhật ký vấn đề.
- [ ] Đã lưu annotation và kiểm tra lại số ảnh/frame.

### Quy trình xuất và kiểm tra

1. Dùng đúng tập ảnh phân công của thành viên; trên CVAT Local tạo task riêng sau khi khóa taxonomy.
2. Gán nhãn độc lập theo guideline và taxonomy cùng phiên bản.
3. Xuất **COCO 1.0**; lưu kết quả đúng hợp đồng bài lab dưới `submission/labels/<mã>.json` (mã 102: `submission/labels/102.json`).
4. Chạy `python scripts/validate_labels.py submission/labels/102.json` và xử lý lỗi nếu có.
5. Gửi kết quả riêng; chỉ tổng hợp nhãn của cả nhóm khi tất cả thành viên đã nộp.
6. QC Lead chạy so sánh IAA, kiểm tra bất đồng và tổ chức calibration theo hướng dẫn `GUIDE.md`.

## 6. Quản lý phiên bản và phê duyệt

| Phiên bản | Nội dung | Trạng thái |
|---|---|---|
| `v0` | Guideline khởi đầu từ giảng viên | Tham khảo |
| `v0.1` | Guideline cá nhân | Đã có bản cá nhân |
| `v1.0` | Guideline nhóm ngày 16/11/2026 | Đã thống nhất theo tài liệu nguồn |
| `v1.0 — bản hoàn thiện đề xuất` | Chuẩn hóa Rule ID, cách đọc mức che, vật nhỏ, ignore, checklist QC | **Chờ nhóm xác nhận** |

**Các điểm cần nhóm xác nhận trước khi thay thế tài liệu chính thức:**

1. Ranh giới 20%/50%/80% của `occluded_level` và cách xử lý ca sát ngưỡng.
2. Áp dụng `min_box_height_px=20` như điều kiện loại trừ box nhỏ; có ngoại lệ nào không.
3. Phạm vi và cách vẽ `ignore_region` (vùng nào, khi nào bỏ qua không vẽ).
4. Tiêu chí ưu tiên để phân biệt `car`/`van`/`truck` khi ảnh không rõ.
5. Thống nhất dùng mã R-01 đến R-07 trong toàn bộ báo cáo QC.

Nếu chỉ sửa lỗi diễn đạt/đánh số mà **không đổi cách gán**, ghi nhận là thay đổi biên tập. Nếu đổi quyết định chọn vật, lớp, box hoặc thuộc tính, áp dụng quy trình thay đổi ngữ nghĩa và calibration theo `GUIDE.md`; không âm thầm ghi đè guideline đã khóa.
