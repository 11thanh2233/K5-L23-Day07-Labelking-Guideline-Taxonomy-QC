# Guideline gán nhãn — v0.1 — 101

> Bản cá nhân để chốt lại các ca mơ hồ trong Pha 1. Đây là phiên bản độc lập trước khi họp nhóm.

- Phiên bản: v0.1
- Ngày: 2026-11-16
- Người viết / duyệt: 101

## 1. Mục tiêu
Mô hình phát hiện người và phương tiện trên ảnh đường phố ở Việt Nam. Mục tiêu là gán đúng từng vật giao thông hiện hữu, không bỏ sót người/xe thật, đồng thời không nhầm với đồ trang trí, mô hình, phản xạ, ảnh quảng cáo hoặc vật quá nhỏ không đủ để phân loại. Sai ở đây sẽ làm tăng nhầm lớp và làm sai trong việc đánh giá mô hình.

## 2. Lớp và thuộc tính
### Lớp
| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Ô tô con, xe hatchback, sedan, SUV, taxi, xe cá nhân có thân riêng. | ô tô chạy trên đường, taxi, xe du lịch | `truck` và `van` nếu là xe thùng/tải lớn hoặc xe chở hàng |
| `truck` | Xe tải, xe chở hàng, xe chở xe, xe có thùng / cabin riêng và kích thước lớn hơn ô tô con. | xe tải, xe chở nhiều xe, xe ben | `car` nếu là xe con bình thường |
| `van` | Xe thùng kín cỡ nhỏ / xe buýt mini / xe thương mại nhỏ. | xe thùng nhỏ, van chở hàng cỡ vừa | `truck` nếu thùng lớn hơn nhiều hoặc có sử dụng cho vận chuyển hàng nặng |
| `motorcycle` | Xe máy, mô tô, xe máy cỡ nhỏ và xe tay ga/tay số. | xe máy đi trên đường, xe máy đậu bên lề | `person` nếu chỉ là người, không phải phương tiện |
| `person` | Người đi bộ, người ngồi trên xe, người trên xe máy hoặc môtô khi phần thân người còn thấy rõ. | người đi bộ, người ngồi sau xe máy, người chở hàng | `motorcycle` nếu chỉ là phần xe, không phải thân người |
| `ignore_region` | Vùng không cần gán từng vật: mô hình, đồ chơi, biển quảng cáo, phản xạ, vật quá nhỏ, vùng không phải đối tượng. | mô hình ô tô trong cửa hàng, tranh quảng cáo, ánh phản chiếu | các vật giao thông thật đang xuất hiện trong không gian đường phố |

Vật không thuộc lớp nào thì không gán. Nếu là phản xạ, mô hình, đồ chơi, biển/chiếu sáng, hay vật nhỏ quá nhỏ để nhận diện rõ, đánh dấu `ignore_region` hoặc bỏ qua nếu không phải phần của đối tượng thật. Không tăng lớp mới trong lượt này.

### Thuộc tính
| Thuộc tính | Giá trị | Ý nghĩa | Ngưỡng cụ thể |
|---|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Mức bị che | `0`: >80% vật thấy rõ; `1`: 50–80% thấy; `2`: 20–50% thấy; `3`: <20% hoặc không nhận biết được hình dạng |
| `truncated` | `no`, `yes` | Vật bị cắt mép ảnh | `yes` nếu có >10% bề rộng hoặc bề cao của box chạm cạnh ảnh |
| `can_review` | `true`, `false` | Cần người khác xem lại | Tick khi chưa chắc về lớp, số box, hoặc cách bao phần nhìn thấy |

## 3. Quy tắc vẽ box
1. Box luôn ôm sát phần có thể nhìn thấy của vật thật, không bao phần ẩn hoặc phần không chắc chắn. Nếu vật bị che, chỉ bao phần còn thấy, không “đoán” phần bị ẩn.
2. Với người và xe máy: nếu người và xe máy đều rõ, vẽ hai box riêng: `person` cho người, `motorcycle` cho xe máy. Không gộp thành 1 box nếu cả hai đều có dạng rõ ràng. Nếu người bị che hoàn toàn hoặc chỉ còn một phần rất nhỏ, có thể bỏ `person` nếu không đủ để nhận diện, chỉ giữ `motorcycle`.
3. Với người ngồi trên xe máy: `person` chỉ tính phần thân người, không bao cả máy; `motorcycle` chỉ bao thân xe và bánh. Nếu một người ngồi sau, mỗi người là một box `person` riêng.
4. Với xe chở xe (`img_002`): xe chở xe là `truck`. Mỗi chiếc xe trên thùng chỉ là `car` nếu rõ là ô tô thật và tách được thành vật riêng; không coi cả tổng thể thùng xe + nhiều xe trên thùng như một box duy nhất.
5. Với vật quá nhỏ: nếu chiều cao box < 20 px hoặc không đủ đặc trưng để nhận diện rõ lớp thì không gán. Ví dụ: chi tiết nhỏ trong cửa hàng, xe mô hình mini, dây treo, biển báo quá nhỏ. Đó là `ignore_region` hoặc bỏ qua.
6. Với tượng, phản chiếu, hình in, đồ chơi, biển quảng cáo: không gán như `car`/`person` nếu không phải vật giao thông thật. Cần để `ignore_region` hoặc đánh dấu `can_review` nếu còn lưỡng lự.
7. Với vật cắt mép ảnh: box vẫn bao phần nhìn thấy, nhưng `truncated=yes` và không kéo dài qua mép nếu không nhìn thấy hoàn toàn.
8. Với đám đông: chỉ gán những người/xe đủ rõ để nhận diện. Nếu quá đông và không thể xác định từng người, dùng `ignore_region` cho khu vực dày đặc hoặc `can_review` nếu cần review nhóm.

## 4. Ca khó
| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002` | Xe chở xe; nhiều ô tô trên thùng và cabin lớn | `R-01` | Theo quy tắc | Xe chở xe là `truck`; từng ô tô trên thùng là `car` nếu rõ và riêng biệt; không gộp cả chồng xe thành một box duy nhất. |
| `img_005` | Những người ngồi trên xe máy, có cả người và xe máy rõ | `R-02` | Theo quy tắc | Gán `motorcycle` cho xe máy và `person` cho từng người trên xe máy; không bao người vào box xe máy. |
| `img_013` | Người đi xe máy bị che/không hoàn toàn rõ do giao thông và chỗ đứng | `R-03` | Theo quy tắc | Nếu phần người vẫn nhận diện được, box `person` chỉ bao phần thực tế nhìn thấy; nếu không rõ thì bỏ `person`, giữ `motorcycle` và đánh `occluded_level=2/3`. |
| `img_036` | Mô hình xe mini/toy trong cửa hàng, rất nhỏ và không phải vật giao thông ngoài đường | `Q-01` | Cần review | Đây là trường hợp dễ lẫn giữa vật thật và mô hình trang trí; nên dùng `ignore_region` nếu không nằm trong đường phố thật, hoặc `can_review` khi còn nghi ngờ. |
| `img_025` / `img_038` | Cảnh người đi bộ chi chít trên đường, nhiều người và xe; một số người nhỏ, một số bị che | `Q-02` | Cần review | Chỉ label khi đủ nhận diện. Vật quá nhỏ hoặc bị che quá nặng để nhận dạng sẽ không gán. |

> Quy tắc rõ ràng: `R-*` là ca đã chốt theo hướng dẫn; `Q-*` là ca cần hỏi reviewer trong cuộc họp nhóm.

## 5. QC và phiên bản
Ngưỡng QC áp dụng: không làm sai lớp đối tượng chính, không gộp người với xe máy, không gán mô hình đồ chơi hoặc phản xạ như vật thật; bất kỳ ca không chắc thì phải dùng `can_review`.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| `v0.1` | Chốt quy tắc dành cho người đi xe máy, xe chở xe, vật quá nhỏ, phản xạ và mô hình | `img_002`, `img_005`, `img_013`, `img_036` |
