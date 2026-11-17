# Guideline gán nhãn — v1.1 (sau calibration)

- Phiên bản: v1.1
- Ngày: 2026-11-17
- Người viết / duyệt: nhóm Labelking — chốt: 103 (QC Lead), kiểm lại: 102 (Guideline Lead)
- Trạng thái: chốt cho bước sửa nhãn Pha 5 và duyệt QC Pha 6
- Taxonomy: `submission/taxonomy_v1.1.json` (8 lớp, 3 thuộc tính, mục `rules` giữ nguyên). So với v1.0: **thêm lớp `bus` và `tuk_tuk`**, viết lại định nghĩa các lớp cũ theo R-11, R-12. Không bỏ lớp nào. Cấu hình CVAT: `cvat/labels_final.json` (sinh bằng `python scripts/make_cvat_labels.py --final`).
- Loại thay đổi: `semantic` (xem `submission/guideline_change.json`). Mọi quy tắc mới áp dụng cho **cả lô 40 ảnh**.

### Cách rà lại cả lô sau khi đổi taxonomy

1. Tạo Project CVAT mới từ `cvat/labels_final.json`; không sửa trên Project cũ (Project cũ thiếu `bus`, `tuk_tuk`).
2. Nạp bản nháp do `python scripts/prepare_calibration.py` chuẩn bị (40 ảnh).
3. Lượt rà riêng cho lớp mới: mở từng ảnh, tìm mọi xe ba bánh và xe buýt lớn. Box nào đang là `car`/`van`/`truck`/`motorcycle` hoặc `ignore_region` trên các xe này thì đổi sang `tuk_tuk`/`bus` và vẽ lại ôm sát theo R-01. Đã biết có tuk-tuk ở `img_016`, `img_035`.
4. Lượt rà thuộc tính theo R-08, R-09 và lượt rà `ignore_region` theo R-10 cho cả 40 ảnh.
5. Người kiểm lại (khác người sửa) đối chiếu lớp `bus`/`tuk_tuk` trên toàn lô, ghi kết quả vào cột `kiem_lai`.

## 0. Vì sao có v1.1 — bằng chứng từ IAA

Kết quả IAA của lượt gán độc lập theo v1.0 (`submission/qc/iaa_summary.md`, 3 người gán, 80/80 lượt, mẫu số 303 cặp box ghép được):

| Chỉ số | Kết quả | Ngưỡng | Đánh giá |
|---|---|---|---|
| IoU trung bình (cặp đã ghép) | 0.818 | ≥ 0.85 | Chưa đạt |
| Đồng thuận lớp | 94.1% | ≥ 95% | Chưa đạt |
| Cùng `occluded_level` | 45.5% | — | Thuộc tính gần như ngẫu nhiên |
| Cùng `truncated` | 58.4% (cặp 101/102 chỉ 32.5%) | — | Hiểu khác nghĩa thuộc tính |
| Box chưa ghép (A/B) | 54/117 | — | Bỏ sót/thừa nhiều |

640 ca bất thường trên 37/40 ảnh: `sai_thuoc_tinh` 200, `bat_dong_ignore` 150, `iou_thap` 129, `bo_sot_thua` 107, `co_can_review` 36, `sai_lop` 18.

Phân tích nguyên nhân (để quyết định sửa guideline hay sửa người gán):

| Nhóm lỗi | Quan sát | Nguyên nhân | Hướng xử lý |
|---|---|---|---|
| `truncated` | 117/130 ca lệch là box **không chạm mép ảnh**; 102 ghi `yes` ở 119/130 ca | v1.0 không nói rõ "cắt" là bởi mép ảnh hay bởi vật khác | Guideline: R-08 |
| `occluded_level` | Lệch cả hai chiều, 102 thường chấm cao hơn, 103 thấp hơn; nhiều ca lệch 2–3 mức | Ngưỡng % khó ước lượng, không có cách đếm và không có luật phá hòa | Guideline: R-09 |
| `ignore_region` | 86 vùng không ghép được, 64 vùng phủ lên vật người kia đã gán riêng; 124/150 vùng cao ≥ 40 px | Dùng `ignore_region` thay cho việc gán vật lớn, tách được | Guideline: R-10, R-11 |
| `bo_sot_thua` | 79/107 vật cao ≥ 40 px (không phải vật nhỏ); 101 và 103 vẽ thêm nhiều nhất | Không quy định rõ xe máy đỗ, người ở hậu cảnh, người ngồi | Guideline: R-13 |
| `sai_lop` car/van/truck | Xe bán tải (img_028, img_016) và xe thùng kiểu HiAce (img_005, img_016) bị chia giữa các lớp | Định nghĩa v1.0 dựa vào "kích thước", không dựa vào kiểu thân xe | Guideline: R-12 |
| `sai_lop` person/car | 102 gán `car` cho người nhỏ ở xa (img_008, img_025, img_029, img_031) | Lỗi thao tác: CVAT chọn sẵn lớp đầu tiên `car` | Người gán: R-14 |
| Xe ngoài taxonomy | Xe đạp bị gán `motorcycle` (img_003, img_029); tuk-tuk bị gán `car`/`van`/`truck` (img_016) | v1.0 không nói phương tiện ngoài 6 lớp xử lý thế nào; taxonomy thiếu lớp cho xe ba bánh, xe buýt | Taxonomy v1.1 thêm `tuk_tuk`, `bus`; guideline: R-11, R-12 |
| `iou_thap` | 129 ca, IoU phần lớn 0.7–0.85 | Không quy định phần nào thuộc vật (gương, mũ, hàng chở) | Guideline: R-01 bổ sung |

## 1. Mục tiêu

Nhãn dùng để huấn luyện và đánh giá mô hình **phát hiện vật 2D** (bounding box) cho người và phương tiện trên ảnh đường phố. Mô hình phải đoán ra **lớp** và **vị trí** của từng vật; thuộc tính `occluded_level`, `truncated` dùng để lọc mẫu khó khi đánh giá, `can_review` chỉ dùng trong quy trình QC.

Một quy tắc tốt trong guideline này phải: (1) hai người đọc độc lập ra cùng một quyết định, (2) kiểm được trên ảnh, (3) có mã `R-xx` để dẫn chiếu trong phiếu quyết định và phiếu QC.

## 2. Lớp và thuộc tính

### 2.1. Lớp

| Lớp | Định nghĩa | Ví dụ | Phản ví dụ / dễ nhầm |
|---|---|---|---|
| `car` | Ô tô chở người có thân liền khoang hành khách, không có thùng hàng hở: sedan, hatchback, SUV, crossover, MPV 7 chỗ, taxi con. | sedan đen sau xe máy (img_016), SUV đỏ (img_028) | Xe bán tải → `truck`; xe thùng hộp cao kiểu HiAce → `van` |
| `truck` | Xe có cabin và **thùng chở hàng tách biệt** (hở hoặc kín): xe tải, xe bán tải (pickup), xe chở xe, xe ben. | xe bán tải nâu (img_028), xe bán tải trắng (img_016), xe chở xe (img_002) | Xe thùng liền thân → `van` |
| `van` | Xe **thân hộp liền một khối** từ đầu tới đuôi, mui cao, cửa trượt hoặc cửa sau lớn, tối đa khoảng 16 chỗ: xe thùng chở hàng, minibus kiểu Toyota HiAce, Ford Transit. | xe trắng kiểu HiAce (img_005, img_016 — kể cả khi có biển TAXI) | MPV/SUV mui thấp → `car`; có thùng tách khỏi cabin → `truck`; thân dài nhiều hàng cửa sổ → `bus` |
| `bus` (mới) | Xe buýt / xe khách **cỡ lớn** (trên 16 chỗ): thân dài, nhiều hàng cửa sổ hành khách, thường có cửa lên xuống ở giữa. | xe buýt thành phố, xe khách đường dài, xe du lịch hai tầng | Minibus thân hộp ≤ 16 chỗ → `van`; xe tải thùng kín → `truck` |
| `tuk_tuk` (mới) | Xe **ba bánh có động cơ** chở khách hoặc hàng: tuk-tuk, xe lam, xe ba gác máy. | tuk-tuk xanh và tuk-tuk trái ảnh (img_016), img_035 | Xe máy kéo thùng rời hai bánh → `motorcycle` (thùng không gồm trong box); xích lô đạp → R-11 |
| `motorcycle` | Xe hai bánh **có động cơ**: xe máy, xe tay ga, mô tô, xe máy điện. Gồm cả xe đang chạy và xe đỗ. | xe máy đỗ hàng loạt (img_003, img_008) | Xe đạp, xe đạp điện có bàn đạp → R-11; xe ba bánh có động cơ → `tuk_tuk` |
| `person` | Người thật đang đi bộ, đứng, ngồi (kể cả ngồi ghế ven đường) hoặc ngồi trên xe máy/xe đạp/tuk-tuk. | người ngồi ghế bãi biển (img_025), người lái xe máy (img_005), người lái tuk-tuk (img_016) | Tượng, ma-nơ-canh, người trong ảnh in/biển quảng cáo, phản chiếu (R-05); người **bên trong ô tô, xe buýt** nhìn qua kính (R-13) |
| `ignore_region` | Vùng loại khỏi chấm điểm, **không phải một vật**. Chỉ dùng theo R-10 và R-11. | đám xe máy đỗ chồng lên nhau ở xa (img_003), xe đạp (img_029) | Một vật đơn lẻ tách được và cao ≥ 20 px → gán box lớp thật |

v1.1 có 7 lớp vật và `ignore_region`. Phương tiện không thuộc lớp nào xử lý theo R-11.

### 2.2. Thuộc tính

| Thuộc tính | Giá trị | Cách chấm (chi tiết ở R-08, R-09) |
|---|---|---|
| `occluded_level` | `0`, `1`, `2`, `3` | Tỉ lệ phần vật **bị vật khác che** (không tính phần nằm ngoài khung ảnh): `0` che < 10%; `1` che 10–40%; `2` che 40–70%; `3` che > 70%. |
| `truncated` | `no`, `yes` | `yes` **chỉ khi** box chạm mép ảnh (cách mép ≤ 2 px) **và** vật còn phần nằm ngoài khung. Bị vật khác che **không** phải `truncated`. |
| `can_review` | `false`, `true` | `true` khi gán độc lập mà không quyết được bằng quy tắc nào. Trong nhãn cuối sau calibration, mọi box đều `false` (R-07). |

`ignore_region` không có thuộc tính.

## 3. Quy tắc

Mã quy tắc ở v1.1 dùng **đúng một** bảng số (bảng ở mục 0 của v1.0 đánh số lệch so với mục 3; v1.1 lấy mục 3 làm chuẩn). R-01 đến R-07 giữ số cũ để dẫn chiếu được về lượt gán v1.0; R-08 đến R-14 là quy tắc mới.

### R-01 — Box ôm sát phần nhìn thấy (bổ sung)

- Mỗi vật hợp lệ đúng **một** box. Bốn cạnh box chạm điểm ảnh ngoài cùng **nhìn thấy được** của vật, sai lệch không quá 2 px; không chừa nền.
- Không suy đoán phần bị che hoặc phần ngoài ảnh.
- Phần **thuộc** vật:
  - `person`: từ đỉnh mũ/nón (kể cả nón lá, mũ bảo hiểm) tới gót chân; gồm tay giơ ra. **Không** gồm đồ cầm/gánh/xách (quang gánh, túi, hàng hóa — img_003).
  - `motorcycle`: từ bánh trước tới bánh sau/đuôi xe, gồm gương, tay lái, giỏ, baga. **Không** gồm người ngồi trên xe (người có box riêng, R-02) và hàng chở nhô ra khỏi xe.
  - `car`/`van`/`truck`: cả thân xe, gồm gương chiếu hậu; với `truck` gồm cả thùng hàng. **Không** gồm hàng hóa/tượng/vật đặt trên thùng nhô cao (tượng ngựa trên thùng img_028 không nằm trong box `truck`).
- Hai người cùng vẽ một vật mà IoU < 0.85 (vật cao ≥ 50 px) hoặc < 0.70 (vật nhỏ hơn) là sai R-01. Khi sửa, **vẽ lại theo quy tắc**, không lấy trung bình hai box.

### R-02 — Người và xe máy là hai vật riêng

Người và xe máy đều rõ thì vẽ 2 box: `person` cho người, `motorcycle` cho xe. Không gộp người + xe thành một box, không để box `person` kéo xuống bao cả xe. Người bị che quá nặng (thấy < 30% thân và không thấy đầu) thì chỉ giữ `motorcycle`. Quy tắc giống hệt áp dụng cho người trên xe đạp (xe đạp xử lý theo R-11).

### R-03 — Xe chở xe

Xe chở xe là `truck`, box gồm cabin và thùng. Từng ô tô trên thùng nhận diện được và tách được là một box `car` riêng (kèm `occluded_level` nếu bị khung thùng che). Không gộp thùng + xe trên thùng thành một box.

### R-04 — Vật bị che / cắt mép ảnh

Box chỉ bao phần nhìn thấy (R-01). Mức che chấm theo R-09, cắt mép theo R-08. Hai thuộc tính **độc lập**: một vật có thể vừa `occluded_level=2` vừa `truncated=yes`.

### R-05 — Vật quá nhỏ / không phải vật thật

- Vật cao < 20 px (`min_box_height_px` trong taxonomy) **không** gán box riêng. Nếu nhiều vật nhỏ như vậy đứng thành cụm, khoanh một `ignore_region` (R-10); một vật nhỏ đơn lẻ thì bỏ qua.
- Tượng, ma-nơ-canh, mô hình, đồ chơi, người/xe trong ảnh in, biển quảng cáo, màn hình, phản chiếu trên kính/nước **không** gán lớp vật. Chỉ khoanh `ignore_region` khi vật giả đó lớn và dễ bị mô hình nhận nhầm (cao ≥ 50 px, hình dạng giống người/xe thật); còn lại bỏ qua.

### R-06 — Đám đông / khu vực dày đặc

Gán box riêng cho từng vật tách được (R-13). Chỉ khi một nhóm ≥ 3 vật chồng lên nhau tới mức không vẽ được box riêng cho từng vật thì khoanh một `ignore_region` cho cả nhóm (R-10). Không dùng `ignore_region` để né việc vẽ nhiều box.

### R-07 — `can_review`

- Khi gán độc lập: tick `can_review=true` khi đã đối chiếu R-01 đến R-14 mà vẫn không quyết được lớp, số box hoặc phạm vi box. Không tick vì lười kiểm hoặc để thay cho việc chấm thuộc tính.
- Sau calibration: mỗi box có cờ đã được quyết định trong `calibration_decisions.csv`; nhãn cuối đặt `can_review=false` cho mọi box. Ca vẫn chưa quyết được thì ghi vào `submission/qc/image_issues.csv`, không để cờ trong nhãn cuối.

### R-08 — `truncated` chỉ theo mép ảnh (mới)

1. Box có chạm mép ảnh không (cạnh box cách mép ≤ 2 px)? **Không** → `truncated=no`, dừng.
2. Có → vật có phần nằm ngoài khung không (ví dụ thân người bị cắt ngang ở mép dưới, nửa xe ở mép trái)? **Có** → `truncated=yes`; vật nằm trọn và chỉ vô tình chạm mép → `no`.
3. Bị vật khác che (người sau xe, xe sau cột) **không bao giờ** là `truncated`; ghi vào `occluded_level`.

Ví dụ: người mặc áo đỏ ở mép phải-dưới img_016 → `yes`; người đứng giữa ảnh bị xe máy che chân → `no`, `occluded_level` theo R-09.

### R-09 — Cách chấm `occluded_level` (mới)

1. Hình dung vật **trong khung ảnh** (bỏ phần ngoài ảnh — đó là R-08).
2. Ước lượng tỉ lệ diện tích bị vật khác che, dùng mốc chia sẵn:
   - `person`: đầu ≈ 15%, thân trên ≈ 35%, hông + chân ≈ 50%.
   - Phương tiện: chia thân xe thành 4 phần bằng nhau theo chiều dài, mỗi phần ≈ 25%.
3. Đổi ra mức: `0` che < 10%; `1` che 10–40%; `2` che 40–70%; `3` che > 70%.
4. Luật phá hòa: phân vân giữa hai mức liền kề → **chọn mức thấp hơn**. Lệch từ 2 mức trở lên giữa hai người → chấm lại từ bước 1, không chọn trung bình.
5. Mốc thường gặp: người ngồi trên xe máy bị xe che hông + chân → `2`; người lái xe máy chỉ thấy đầu và vai sau lưng người khác → `3`; xe máy đỗ trong hàng, thấy ½ thân → `2`.

### R-10 — Khi nào dùng `ignore_region` (mới)

Chỉ khoanh `ignore_region` trong 4 trường hợp:

1. Cụm ≥ 3 vật chồng lên nhau, không vẽ được box riêng cho từng vật (R-06).
2. Cụm vật cao < 20 px (R-05).
3. Phương tiện ngoài taxonomy (R-11).
4. Vật giả lớn dễ nhầm (R-05).

Cách vẽ: một vùng ôm sát toàn cụm; **không** phủ lên vật đã có box riêng; không lồng nhiều vùng ignore vào nhau. Vật tách được và cao ≥ 20 px luôn được gán box lớp thật, kể cả khi ở gần một vùng ignore.

### R-11 — Phương tiện ngoài taxonomy (mới)

Xe buýt lớn và xe ba bánh có động cơ **đã có lớp** từ v1.1 (`bus`, `tuk_tuk`) — không thuộc R-11. Taxonomy v1.1 vẫn chưa có lớp cho **xe đạp, xe đạp điện có bàn đạp, xích lô đạp, xe kéo tay**. Với các xe này:

- Khoanh `ignore_region` ôm sát xe (không gán `motorcycle` hay lớp xe khác). Lý do: mô hình không bị phạt khi phát hiện chúng, và không học sai lớp.
- Người ngồi/đứng trên xe vẫn gán `person` riêng theo R-02 nếu nhìn thấy rõ.

Đề xuất cho phiên bản sau: bổ sung lớp `bicycle` (v1.2 trở đi) nếu dữ liệu có đủ mẫu.

### R-12 — Phân biệt các lớp xe (mới)

Hỏi theo thứ tự, dừng ở câu trả lời "có" đầu tiên:

1. Xe **ba bánh có động cơ**? → `tuk_tuk`.
2. Xe hai bánh có động cơ? → `motorcycle` (xe hai bánh không động cơ → R-11).
3. Có thùng chở hàng **tách khỏi cabin** (thùng hở như bán tải, hoặc thùng kín đặt sau cabin)? → `truck`.
4. Thân dài chở khách, **nhiều hàng cửa sổ** (trên 16 chỗ)? → `bus`.
5. Thân xe là **một hộp liền**, mui cao gần thẳng đứng, không có nắp ca-pô dài phía trước? → `van`.
6. Còn lại (ô tô chở người có ca-pô, mui thấp hoặc SUV) → `car`.

Không dùng kích thước trong ảnh để chọn lớp (xe ở xa trông nhỏ). Biển "TAXI" không đổi lớp: taxi kiểu HiAce là `van`, taxi sedan là `car`.

### R-13 — Gán đủ mọi vật hợp lệ (mới)

- Mọi `person`, `motorcycle`, `tuk_tuk`, `car`, `van`, `truck`, `bus` cao ≥ 20 px, nhìn thấy ≥ 30% thân (hoặc thấy đầu với `person`) đều phải có box, **kể cả**: xe máy đỗ, người ở hậu cảnh, người ngồi ghế, người đứng trong cửa hàng nhìn rõ từ đường.
- **Không** gán người ngồi bên trong ô tô/xe buýt nhìn qua kính (vật thật là chiếc xe).
- Bỏ sót do không nhìn kỹ hậu cảnh là lỗi người gán: trước khi chuyển ảnh, quét lại ảnh theo 4 góc phần tư.

### R-14 — Kiểm lớp sau mỗi box (mới, quy trình)

CVAT chọn sẵn lớp đầu tiên (`car`) cho box mới. Sau khi vẽ mỗi box, kiểm lại nhãn lớp trên box trước khi vẽ box tiếp. Khi QC, box `car` có hình dạng người (cao > rộng, cao < 80 px) được kiểm riêng.

## 4. Ca khó và quyết định

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| `img_002` | Xe chở xe, có ô tô trên thùng | R-03 | `truck` cho xe chở; `car` cho từng xe trên thùng nếu tách được | Từng ô tô là vật riêng mô hình phải thấy |
| `img_003` | Người đứng cạnh xe đạp, quang gánh | R-01, R-11 | `person` không bao quang gánh; xe đạp → `ignore_region` | Đồ mang theo không phải người; xe đạp ngoài taxonomy |
| `img_003`, `img_008` | Hàng xe máy đỗ chồng nhau | R-06, R-10, R-13 | Xe tách được và cao ≥ 20 px → box riêng; đoạn chồng kín ở xa → một `ignore_region` | Không dùng ignore thay cho xe tách được |
| `img_005` | Xe thùng trắng kiểu HiAce sau người đi xe máy | R-12 | `van` | Thân hộp liền, không ca-pô dài |
| `img_005` | Nhiều người đi xe máy chồng lên nhau ở cận cảnh | R-02, R-09 | Box riêng từng người và từng xe; người sau chỉ thấy đầu vai → `occluded_level=3` | Chấm theo mốc đầu/thân/chân |
| `img_016`, `img_035` | Tuk-tuk xanh và tuk-tuk trái ảnh | R-12 | `tuk_tuk` ôm sát xe; người lái gán `person` riêng | Lớp mới của taxonomy v1.1 |
| `img_016` | Xe bán tải trắng (MIGHTY-X) | R-12 | `truck` | Có thùng tách khỏi cabin |
| `img_016` | Người áo đỏ ở mép phải-dưới | R-08 | `truncated=yes` | Chạm mép và bị cắt ngoài khung |
| `img_025` | Người ngồi ghế ven bãi biển, nhỏ | R-13, R-14 | `person` (không phải `car`) | Người thật; lỗi lớp mặc định của CVAT |
| `img_028` | Xe bán tải cổ chở tượng ngựa | R-12, R-01, R-05 | `truck`; box không bao tượng; tượng không gán | Bán tải là truck; tượng không phải vật thật |
| `img_029` | Người dắt/đi xe đạp chở ống dài | R-02, R-11 | `person` + `ignore_region` cho xe đạp | Không gán xe đạp là `motorcycle` |
| `img_036` | Mô hình / đồ chơi / vật rất nhỏ | R-05 | Không gán như vật thật | Không phải đối tượng giao thông |
| `img_013`, `img_038` | Người bị che nặng | R-02, R-09, R-13 | Thấy đầu hoặc ≥ 30% thân → gán, `occluded_level=3`; kém hơn → bỏ | Ngưỡng nhìn thấy đo được |

## 5. QC và phiên bản

### QC áp dụng

- Ngưỡng trong mục `rules` của `submission/taxonomy.json` giữ nguyên: `min_box_height_px=20`, `iou_thr_large=0.85` (vật ≥ `large_px=50`), `iou_thr_small=0.70`, `iaa_iou=0.85`, `iaa_class=0.95`, `error_rate_img_max=0.02`, `match_iou=0.5`.
- Mọi quyết định calibration ghi ở `submission/qc/calibration_decisions.csv`, mỗi ca một dòng, có mã quy tắc của v1.1.
- Do thay đổi `semantic`, **cả lô 40 ảnh** được rà lại theo R-08 đến R-14, không chỉ 37 ảnh bị cờ.
- Phiếu QC (`qc_review.csv`) ghi `rule_id` theo mã của v1.1.

### Lịch sử phiên bản

| Phiên bản | Thay đổi | Lý do |
|---|---|---|
| `v0` | Bản gốc từ giảng viên | Chưa đủ chi tiết |
| `v0.1` | Bản cá nhân 101, 102, 103 | Mỗi thành viên đề xuất quy tắc riêng |
| `v1.0` | Chốt quy tắc nhóm R-01 đến R-07 | Người đi xe máy, xe chở xe, vật quá nhỏ, ignore region |
| `v1.1` | Taxonomy v1.1: thêm lớp `bus`, `tuk_tuk`. Thêm R-08 đến R-14; bổ sung R-01, R-05, R-06, R-07; định nghĩa lại lớp `car`/`van`/`truck`/`motorcycle`; ngưỡng mới cho `occluded_level`; thống nhất một bảng mã quy tắc | IAA v1.0 chưa đạt (IoU 0.818, lớp 94.1%, occluded 45.5%, truncated 58.4%); 640 ca trên 37 ảnh |

## 6. Mã quy tắc

- `R-01`: Box ôm sát phần nhìn thấy; phần nào thuộc vật.
- `R-02`: Người và xe là hai vật riêng.
- `R-03`: Xe chở xe và xe trên thùng.
- `R-04`: Bị che / cắt mép là hai thuộc tính độc lập.
- `R-05`: Vật cao < 20 px / vật không phải vật thật.
- `R-06`: Đám đông / khu vực dày đặc.
- `R-07`: `can_review` khi gán và sau calibration.
- `R-08`: `truncated` chỉ theo mép ảnh.
- `R-09`: Cách chấm `occluded_level`.
- `R-10`: Khi nào dùng `ignore_region`.
- `R-11`: Phương tiện ngoài taxonomy.
- `R-12`: Phân biệt các lớp xe (`tuk_tuk`, `motorcycle`, `truck`, `bus`, `van`, `car`).
- `R-13`: Gán đủ mọi vật hợp lệ.
- `R-14`: Kiểm lớp sau mỗi box.
