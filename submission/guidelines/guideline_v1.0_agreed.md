# Guideline gán nhãn — v1.0 (đã thống nhất nhóm)

- Phiên bản: v1.0
- Ngày: 2026-11-16
- Người viết / duyệt: nhóm Labelking
- Trạng thái: chốt cho gán nhãn độc lập

## 0. Bản chốt và điểm bất đồng đã giải quyết

Các bản cá nhân đã thống nhất trên các điểm sau:

- `R-01`: Người và xe máy là hai vật khác nhau. Nếu người và xe máy đều rõ, gán hai box riêng: `person` + `motorcycle`. Nếu người bị che quá nặng hoặc không đủ nhận dạng, chỉ gán `motorcycle` khi phần xe còn rõ.
- `R-02`: Xe chở xe thuộc lớp `truck`; nếu trên thùng có ô tô riêng và rõ ràng, mỗi ô tô được gán `car` nếu tách được vật đó. Không gộp cả khối xe chở xe thành một box duy nhất.
- `R-03`: Vật quá nhỏ, phản xạ, mô hình, đồ chơi, biển quảng cáo không phải vật thật thì không gán như phương tiện/ người. Gán `ignore_region` nếu nơi đó là khu vực bỏ qua hoặc bỏ qua nếu không đủ dữ kiện.
- `R-04`: Box chỉ bao phần nhìn thấy; không suy đoán phần ẩn. Nếu vật bị che có phần không nhìn thấy, không kéo box ra ngoài phần thật đang thấy.
- `R-05`: `can_review` dùng cho trường hợp mơ hồ về lớp, số box, hoặc cách bao vùng; không dùng để lấp chỗ chưa chắc mà không có căn cứ.

## 1. Mục tiêu
Mô hình phát hiện người và phương tiện trên ảnh đường phố ở Việt Nam để phục vụ huấn luyện và đánh giá trình tự nhận diện đối tượng trong cảnh giao thông 2D. Mục tiêu của guideline là giảm sai lớp, giảm gộp hai vật thành một box, và tránh label các vật không phải người/xe thật như mô hình, đồ chơi, phản xạ hoặc vật quá nhỏ. Nếu không biết chắc, cần dùng `can_review` và để người review chốt.

## 2. Lớp và thuộc tính

### 2.1. Lớp
| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con, xe du lịch, SUV, xe cá nhân có thân riêng và hình dạng rõ như ô tô. | sedan, SUV, hatchback, taxi | `truck` nếu là xe tải / xe chở hàng lớn hơn; `van` nếu là xe thùng kín cỡ nhỏ |
| `truck` | Xe tải, xe chở hàng, xe chở xe hoặc phương tiện có thùng / cabin riêng lớn hơn xe con. | xe tải, xe chở xe | `car` nếu là xe con thường; `van` nếu kích thước nhỏ hơn rõ rệt |
| `van` | Xe thùng kín cỡ nhỏ / chuyên vận chuyển nhỏ. | van chở hàng cỡ nhỏ, xe thùng mini | `truck` nếu lớn hơn nhiều; `car` nếu là xe con thường |
| `motorcycle` | Xe máy, mô tô, các loại xe 2 bánh. | xe máy, mô tô, xe đạp | `person` nếu chỉ là người, không có phương tiện |
| `person` | Người đi bộ hoặc người trên phương tiện, chỉ gán khi phần thân người còn rõ và có thể nhận diện được. | người đi bộ, người ngồi trên xe máy | `motorcycle` nếu chỉ là phương tiện, không thấy người |
| `ignore_region` | Vùng không cần gán từng vật: phản xạ, mô hình, đồ chơi, biển quảng cáo, vật quá nhỏ, khu vực dày đặc không tách được rõ. | mô hình ô tô trong cửa hàng, vật quá nhỏ, phản xạ | đối tượng thật trên đường phố |

Vật không thuộc lớp nào thì không gán. Nếu là hình in, mô hình, đồ chơi, phản xạ, vật quá nhỏ hoặc không đủ thông tin để phân biệt lớp, không thêm lớp mới và không đoán nhầm thành `car`/`person`/`motorcycle`.

### 2.2. Thuộc tính
| Thuộc tính | Giá trị | Ý nghĩa và ngưỡng |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Mức bị che: `0` thấy rõ > 80%; `1` che ít 50–80%; `2` che nhiều 20–50%; `3` che cực nhiều < 20% hoặc gần không nhận biết được. |
| `truncated` | `no`, `yes` | `yes` nếu vật bị cắt bởi mép ảnh, có phần hình không còn trong khung hình. |
| `can_review` | `false`, `true` | `true` khi cần reviewer xác nhận lớp/box/thuộc tính; mặc định `false` khi chắc chắn. |

## 3. Quy tắc vẽ box

### R-01 — Box ôm sát phần nhìn thấy
Mỗi vật hợp lệ có một box riêng, ôm sát phần thực tế nhìn thấy. Không kéo dài ngoài phần vật còn thấy. Không bao phần ẩn hoặc phần chỉ suy đoán.

### R-02 — Người và xe máy là hai vật riêng
Nếu người và xe máy đều rõ, vẽ 2 box riêng: `person` cho người, `motorcycle` cho xe máy. Không gộp một người + xe máy thành 1 box. Nếu người bị che quá nặng, chỉ gán `person` khi phần thân người còn đủ rõ; nếu không, chỉ giữ `motorcycle` nếu xe máy còn rõ.

### R-03 — Xe chở xe
Vật lớn kéo theo xe khác trên thùng là `truck` khi đó là phương tiện chở xe. Nếu trên thùng có ô tô rõ ràng và tách được, từng ô tô là `car` riêng. Không coi cả khối thùng + xe trên thùng là 1 vật duy nhất nếu từng xe có thể nhận diện riêng.

### R-04 — Vật bị che / cắt mép ảnh
- Vật bị che: box chỉ bao phần còn thấy; `occluded_level` phù hợp với mức che.
- Vật cắt mép ảnh: box dừng ở mép ảnh và đặt `truncated=yes`.
- Không mở rộng box giả định ra ngoài hình ảnh.

### R-05 — Vật quá nhỏ / không phải vật thật
Nếu vật quá nhỏ để nhận diện lớp rõ ràng, hoặc là mô hình, đồ chơi, phản xạ, hình in, biển quảng cáo, không gán như đối tượng thật. Dùng `ignore_region` cho khu vực bỏ qua hoặc bỏ qua nếu chưa đủ căn cứ.

### R-06 — Đám đông / khu vực dày đặc
Chỉ gán đối tượng khi đủ rõ để phân loại. Nếu đám đông quá dày và không tách được các vật rõ ràng, ưu tiên không gán hoặc dùng `ignore_region` cho vùng đó.

### R-07 — `can_review`
Nếu tồn tại một trong các trường hợp sau, tick `can_review=true`: không chắc về lớp, số box, phần nào cần bao, hoặc vật bị che quá nặng. Ngoài ra, dùng `can_review` để báo “cần người khác kiểm lại” thay vì đoán mò.

## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002` | Xe chở xe; thùng có nhiều xe như ô tô trên đó | `R-03` | `truck` cho xe chở xe; `car` cho từng xe trên thùng nếu rõ | Phần thân chính là xe chở xe, từng xe riêng chỉ được label khi rõ và tách được |
| `img_005` | Người ngồi trên xe máy và xe máy rõ | `R-02` | 2 box: `motorcycle` + `person` | Người và phương tiện là hai vật riêng |
| `img_013` | Người đi xe máy bị che / không rõ | `R-02`, `R-04`, `R-07` | Chỉ giữ box nào còn đủ rõ; nếu không rõ, không đoán thêm | Không suy đoán phần ẩn; nếu không chắc có thể `can_review` |
| `img_036` | Mô hình / đồ chơi / vật rất nhỏ trong cảnh | `R-05` | Không gán như vật thật | Đây không phải đối tượng chính của cảnh đường phố |
| `img_025`, `img_038` | Nhiều người, vật nhỏ/che nặng | `R-06`, `R-07` | Chỉ label thứ đủ rõ; còn lại bỏ qua hoặc `can_review` | Không gán những đối tượng không xác định chắc chắn |

> Ca “theo quy tắc” là các trường hợp đạt ít nhất một `R-*` rõ ràng. Ca “cần hỏi reviewer” là những trường hợp còn mơ hồ hoặc có khả năng sai do không đủ dữ kiện, thường gắn với `can_review=true`.

## 5. QC và phiên bản

### QC áp dụng
Dùng tiêu chuẩn đã thống nhất từ taxonomy v1.0, nhưng không sửa mục `rules` trong file taxonomy. Các ngưỡng có sẵn trong `submission/taxonomy.json` phải được giữ nguyên để đảm bảo tính nhất quán khi chạy validation và IAA.

### Lịch sử phiên bản
| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| `v0` | Bản gốc từ giảng viên | Chưa đủ chi tiết |
| `v0.1` | Bản cá nhân của từng người | Mỗi thành viên đã đề xuất quy tắc riêng |
| `v1.0` | Chốt quy tắc nhóm | Chốt các trường hợp bất đồng chính: người xe máy, xe chở xe, vật quá nhỏ, ignore region |

## 6. Mã quy tắc trọng tâm
- `R-01`: Box ôm sát phần nhìn thấy.
- `R-02`: Người và xe máy là hai vật riêng.
- `R-03`: Xe chở xe và xe trên thùng.
- `R-04`: Bị che / cắt mép ảnh.
- `R-05`: Vật quá nhỏ / không phải vật thật.
- `R-06`: Đám đông / khu vực dày đặc.
- `R-07`: Dùng `can_review` khi mơ hồ.
