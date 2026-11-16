# Guideline gán nhãn — v0.1 (cá nhân) — 103

- Phiên bản: v0.1-103
- Ngày: 2026-11-16
- Người viết / duyệt: 103
- Phạm vi: 40 ảnh `data/images/img_001.jpg` … `img_040.jpg`, box 2D, CVAT → COCO 1.0

## 1. Mục tiêu

Nhãn dùng huấn luyện mô hình **phát hiện người và phương tiện cơ giới đang tham gia giao thông** trên ảnh 2D (camera giao thông / hỗ trợ lái).

- Nguy hiểm nhất là **bỏ sót người thật** (nhất là người đi xe máy, người đi bộ băng qua đường) → ưu tiên recall cho `person` và `motorcycle`.
- Nguy hiểm thứ hai là **dạy mô hình báo động giả** với vật không phải người/xe thật: tượng, ma-nơ-canh, ảnh trên biển quảng cáo, đồ chơi, ảnh phản chiếu → những vật này **không gán**.
- Box sai lớp giữa `car` / `van` / `truck` ít nguy hiểm hơn bỏ sót, nhưng làm giảm IAA → cần định nghĩa ranh giới rõ (mục 2).

## 2. Lớp và thuộc tính

### Lớp

| Lớp | Định nghĩa (một câu) | Ví dụ | Phản ví dụ / dễ nhầm với |
|---|---|---|---|
| `car` | Xe ô tô chở người cỡ nhỏ, khoang hành khách liền thân, ≤ 9 chỗ: sedan, hatchback, SUV, wagon, taxi. | img_015 (xe đỏ, xe bạc), img_023 (sedan đen), img_024 (wagon đen + xe vàng), img_040 (taxi xanh) | Pickup có thùng hở → `truck`; xe khách / minibus nhiều hàng ghế → không gán (R-07) |
| `truck` | Xe chở hàng có **cabin tách khỏi thùng/sàn hàng**: pickup, xe tải thùng, xe tải bạt, đầu kéo + rơ-moóc. | img_001 (pickup Suzuki), img_002 (xe chở ô tô), img_007 (Hilux + Isuzu thùng), img_012, img_028, img_036, img_037 | Van kín liền khối → `van`; pickup có nắp thùng kín (img_037) vẫn là `truck` vì cabin tách thùng |
| `van` | Xe thùng kín **liền một khối** từ đầu đến đuôi, cỡ nhỏ, cửa trượt hông hoặc cửa sau (kiểu Toyota Hiace, Ford Transit). | img_005 (van bạc 51LD), img_016 (van trắng bên phải) | Minibus/coach có cửa lên xuống kiểu xe buýt (img_009) → không gán (R-07) |
| `motorcycle` | Xe hai bánh có động cơ: xe máy, xe tay ga, mô tô; xe có thùng/sidecar gắn kèm tính là **một** xe máy. | img_005, img_006, img_010, img_021, img_026, img_030, img_016 (Vespa), img_022 (có sidecar) | Xe đạp, xích lô, tuk-tuk, xe ba bánh chở hàng → không gán (R-07) |
| `person` | Người thật nhìn thấy được, mọi tư thế: đi bộ, đứng, ngồi, người lái/người ngồi sau xe máy, người đạp xe/xích lô. | img_001, img_014, img_026 (2 người trên 1 xe), img_034, img_032 | Tượng (img_017), ma-nơ-canh (img_033), ảnh người trên biển/tranh (img_018, img_026 nền, img_030 poster) → không gán (R-06) |
| `ignore_region` | Vùng có nhiều người/xe thật nhưng **không tách được từng cá thể** hoặc quá nhỏ; bỏ sót trong vùng này không tính lỗi. | img_021 (dòng xe máy phía xa), img_030 (bãi xe phía sau) | Không dùng để "che" vật thuộc lớp rõ ràng mà mình ngại vẽ |

**Vật không thuộc lớp nào** (xe buýt, minibus/coach, tuk-tuk, xích lô, xe đạp, auto-rickshaw, động vật, đồ vật): **không gán box, không vẽ ignore_region**. Người ngồi/lái trên các xe đó vẫn gán `person` nếu thấy được (R-07). Nếu không chắc vật có thuộc lớp hay không → gán theo lớp gần nhất và tick `can_review`.

### Thuộc tính

| Thuộc tính | Mức | Nghĩa và ngưỡng đo |
|---|---|---|
| `occluded_level` | `0` | Bị che **< 10%** diện tích ước lượng của vật. |
| | `1` | Bị che **10% – < 40%**. |
| | `2` | Bị che **40% – 80%**. |
| | `3` | Bị che **> 80%**, hoặc không ước lượng được phần bị che (quá tối, mờ do chuyển động mạnh). |
| `truncated` | `no` | Toàn bộ vật nằm trong khung ảnh. |
| | `yes` | Một phần vật **ra ngoài mép ảnh** (box chạm mép và vật rõ ràng còn tiếp). Phần ngoài mép **không** tính vào `occluded_level`. |
| `can_review` | tick | Không chắc lớp, không chắc vật có phải thật, hoặc không chắc ranh giới box. Ghi lý do trong `image_issues.csv` nếu là vấn đề cấp ảnh. |

Ghi chú đo che khuất:
- Che bởi **vật khác trong ảnh** (người, xe khác, cột, hàng hóa) mới tính. Phần ra ngoài mép ảnh chỉ tính vào `truncated`.
- Hàng rào song thưa / lưới (img_018): chỉ tính phần bị che thật sự; tối đa `1` nếu vẫn nhìn rõ hình dạng xe qua song.
- Người ngồi trên xe máy che một phần xe: tính như che bình thường cho box `motorcycle`.

## 3. Quy tắc vẽ box

- **R-01 — Ôm sát phần nhìn thấy.** Box ôm sát pixel nhìn thấy của vật (sai số ≤ 2–3 px). Không ước lượng phần bị che phía sau vật khác. Gương chiếu hậu, ăng-ten mảnh không cần đưa vào nếu làm box rộng thêm rõ rệt.
- **R-02 — Người và xe máy là hai loại box riêng.** Mỗi xe máy một box `motorcycle` (ôm thân xe + bánh + phần người che không làm thay đổi ranh giới xe). Mỗi người trên xe một box `person` riêng (lái và ngồi sau, kể cả trẻ em). Box `person` gồm mũ bảo hiểm và phần thân/chân nhìn thấy, kể cả phần chồng lên xe. Thử trên img_026: 1 `motorcycle` + 2 `person`; img_010 xe giữa: 1 `motorcycle` + 2 `person`.
- **R-03 — Hàng hóa không thuộc box.** Hàng chở trên xe máy (ống dài img_029, sọt, túi) hoặc đồ người mang (quang gánh img_003, túi xách) **không** mở rộng box `motorcycle`/`person`. Hàng hóa che xe → tính vào `occluded_level`. Riêng `truck`: hàng trong thùng nằm trong box vì box ôm thân xe.
- **R-04 — Vật bị cắt mép ảnh.** Vẽ đến mép ảnh, đặt `truncated=yes`. Ví dụ: img_015 xe đỏ và xe bạc, img_040 taxi và người đội mũ.
- **R-05 — Vật quá nhỏ.** Vật có chiều cao box **< 20 px** (theo `min_box_height_px` trong taxonomy) không gán từng box. Nếu có cụm ≥ 3 vật nhỏ như vậy liền nhau → một `ignore_region` bao cụm. Vật ≥ 20 px nhưng thấy rõ thì phải gán.
- **R-06 — Không phải vật thật thì không gán.** Tượng, ma-nơ-canh, đồ chơi, mô hình, bia mộ hình xe, ảnh in / biển quảng cáo / tranh tường, **ảnh phản chiếu** trong gương, kính, mặt đường ướt: không gán, không vẽ ignore_region.
- **R-07 — Phương tiện ngoài taxonomy.** Xe buýt, minibus/coach, tuk-tuk, xích lô, xe đạp, auto-rickshaw: không gán box. Người trên các xe này vẫn gán `person` nếu thấy được thân người (không sau kính kín).
- **R-08 — Người trong xe.** Người ngồi sau kính kín của ô tô/van/truck/xe buýt: **không** gán. Người ở khoang hở nhìn rõ (lái tuk-tuk img_004, lái xe diễu hành img_019): gán `person`.
- **R-09 — Xe chủ (ego).** Phần xe của người chụp (khung gương, cửa, nắp capo trong img_020): không gán.
- **R-10 — Xe chở xe.** Đầu kéo + rơ-moóc chở xe là **một** box `truck` bao cả cabin và giàn chở (img_002). Mỗi ô tô thật đặt trên giàn gán `car` riêng, che khuất theo giàn sắt. Ô tô đặt trên nóc ô tô khác (img_024): cả hai đều gán `car`.
- **R-11 — Đám đông / bãi xe dày.** Gán từng người/xe khi tách được ranh giới (thấy đầu + vai với người, thấy bánh hoặc yên + đầu xe với xe máy). Phần phía sau không tách được → một `ignore_region` (img_021 phía xa, img_030 hàng sau, img_019 khán giả phía sau rào nếu quá dày).
- **R-12 — Mờ do chuyển động.** Gán nếu nhận ra được lớp; box ôm vùng thân vật rõ nhất, không ôm hết vệt mờ; `occluded_level=3` nếu không ước lượng được biên, kèm `can_review` (img_014 người đi xe máy mờ, img_015 xe mờ phía sau).

## 4. Ca khó

Phân biệt: **[QT]** = loại/quyết theo quy tắc ở trên; **[HỎI]** = cần reviewer/nhóm chốt ở Pha 2.

| Ảnh | Tình huống | Rule ID | Quyết định | Lý do |
|---|---|---|---|---|
| img_002 | Xe đầu kéo chở 7–8 ô tô trên giàn 2 tầng | R-10 | [HỎI] 1 `truck` (cabin + giàn) + mỗi ô tô một `car`, occluded theo giàn | Ô tô là vật thật, mô hình nên nhận ra; nhưng nhóm có thể muốn coi là hàng hóa → cần chốt chung |
| img_024 | Xe vàng đặt trên nóc wagon đen, trong bảo tàng | R-10 | [QT] Cả hai `car` | Đều là ô tô thật, không phải mô hình |
| img_017 | Tượng người cưỡi ngựa đội nón giao thông, có chim mòng biển | R-06 | [QT] Không gán gì, ảnh vẫn có trong COCO | Tượng không phải người thật |
| img_033 | Ma-nơ-canh trong tủ kính, phản chiếu xe tải trên kính | R-06 | [QT] Không gán | Ma-nơ-canh + ảnh phản chiếu |
| img_018 | Ảnh người trên biển bầu cử; ô tô sau hàng rào | R-06, R-01 | [QT] Không gán người trên biển; gán từng `car` sau rào, occluded tối đa 1 | Người in trên biển không phải người thật |
| img_020 | Gương chiếu hậu phản chiếu đường, xe, cầu vồng | R-06, R-09 | [QT] Không gán gì | Toàn bộ là ảnh phản chiếu + xe chủ |
| img_027 | Bia mộ hình xe bán tải bằng đá | R-06 | [QT] Không gán | Không phải xe thật |
| img_028 | Tượng ngựa đứng trên thùng pickup cổ thật | R-06, R-03 | [QT] 1 `truck`, tượng ngựa không gán; ô tô đỏ phía sau gán `car` | Pickup thật; ngựa là tượng |
| img_038 | Tủ kính đồ chơi, mô hình ô tô | R-06 | [QT] Không gán | Mô hình đồ chơi |
| img_011 | Tượng/trang phục "Predator" và các xe máy trang trí bằng kim loại | R-06 | [HỎI] Tượng không gán; xe máy kim loại gán `motorcycle` + `can_review` | Không chắc các xe là xe chạy được hay tác phẩm điêu khắc |
| img_019 | Xe diễu hành hình ô tô (có biển số), người lái + linh vật chuột; khán giả đông sau rào | R-08, R-06, R-11 | [HỎI] Xe → `car` + `can_review`; người lái `person`; linh vật không gán; khán giả tách được thì gán, phần dày → `ignore_region` | Xe có biển số, chạy trên đường nhưng hình dáng là mô hình |
| img_026 | Đôi nam nữ trên xe máy; tranh tường cảng biển phía sau | R-02, R-06 | [QT] 1 `motorcycle` + 2 `person`; tranh không gán | Đúng ca chuẩn người đi xe máy |
| img_029 | Người đi xe máy vác ống dài, người đi xe đạp bên cạnh | R-03, R-07 | [QT] `motorcycle` không gồm ống; 2 `person`; xe đạp không gán | Hàng hóa không thuộc box; xe đạp ngoài taxonomy |
| img_003 | Người gánh quang gánh, xe đạp, xe máy | R-03, R-07 | [QT] `person` không gồm quang gánh; xe đạp không gán | Đồ mang theo không thuộc box |
| img_022 | Ảnh đen trắng cũ: xe máy có sidecar trên đường rừng | R-02 | [QT] 1 `motorcycle` bao cả sidecar + 1 `person` | Sidecar gắn liền, coi là một xe |
| img_004 | Hai tuk-tuk có người lái | R-07, R-08 | [HỎI] Tuk-tuk không gán; người lái thấy rõ → `person` | Tuk-tuk là xe 3 bánh có mui, không khớp lớp nào; cần nhóm chốt có thêm lớp hay không |
| img_016 | Tuk-tuk, xe tay ga Vespa, van trắng, người phụ nữ cắt mép dưới | R-07, R-04 | [QT] Vespa `motorcycle`; van `van`; tuk-tuk không gán; người phụ nữ `person`, `truncated=yes` | |
| img_035 | Auto-rickshaw chở hàng cao, xe máy, ô tô | R-07, R-03 | [QT] Auto-rickshaw không gán; xe máy + người gán; ô tô trắng `car` | |
| img_023 | Xích lô đi giữa đường, sedan đen | R-07 | [QT] Xích lô không gán, người đạp xích lô `person`, sedan `car` | |
| img_009 | Minibus/coach trắng, cửa kiểu xe buýt | R-07 | [HỎI] Không gán (coi là xe buýt) | Ranh giới van ↔ minibus cần nhóm chốt |
| img_037 | Pickup có nắp thùng kín cao | R-01 | [QT] `truck` | Cabin tách thùng, không phải van liền khối |
| img_021 | Dòng xe máy rất dày, phía xa nhỏ dần | R-11, R-05 | [QT] Gán từng xe/người phía trước; phía xa → `ignore_region` | Không tách được cá thể |
| img_030 | Bãi xe máy dày, xe chồng lên nhau | R-11 | [QT] Gán từng xe hàng trước; hàng sau → `ignore_region` | |
| img_032 | Hàng người chờ xe buýt (~40 người), xe hơi cắt mép trái | R-11, R-04 | [HỎI] Gán từng người tách được; cụm chồng lấn → `ignore_region`; xe trái `car`, `truncated=yes` | Số box lớn, dễ lệch IAA → cần chốt ngưỡng "tách được" |
| img_014 | Người đi bộ rõ nét, người đi xe máy mờ chuyển động | R-12 | [QT] 2 người đi bộ `person` occluded 0; xe/người mờ gán nếu nhận ra, `can_review` | |
| img_031 | Đêm mưa, phản chiếu đèn và xe trên mặt đường | R-06 | [QT] Không gán phản chiếu trên mặt đường | |
| img_040 | Người đội mũ cận cảnh, taxi, tuk-tuk, xe buýt nền | R-04, R-07 | [QT] `person` + `car` taxi `truncated=yes`; tuk-tuk/xe buýt không gán | |

Ca chưa chốt khi gán: tick `can_review` trên box hoặc ghi `submission/qc/image_issues.csv` (cột `image,annotator,region,note`).

## 5. QC và phiên bản

Ngưỡng QC (giữ nguyên mục `rules` trong `taxonomy.json`):

| Chỉ số | Ngưỡng |
|---|---|
| Chiều cao box tối thiểu | 20 px |
| IoU ghép cặp khi so sánh | ≥ 0.5 |
| IAA — IoU trung bình các cặp ghép | ≥ 0.85 |
| IAA — % cùng lớp trên các cặp ghép | ≥ 95% |
| IoU chấp nhận khi QC: vật lớn (> 50 px) / vật nhỏ | ≥ 0.85 / ≥ 0.7 |
| Tỉ lệ ảnh lỗi tối đa để Release | ≤ 2% |

- Ca mơ hồ: người gán tick `can_review`; Guideline Lead (Người 2) và QC Lead (Người 3) chốt ở Pha 2 / Pha 5, ghi vào `calibration_decisions.csv` với mã R-xx.
- Thay đổi chỉ câu chữ → `editorial`; thay đổi cách chọn vật/lớp/box/thuộc tính → `semantic`, tăng phiên bản và kiểm lại cả lô.

| Phiên bản | Thay đổi | Lý do (ca nào) |
|---|---|---|
| v0 | Bản khởi đầu của giảng viên | — |
| v0.1-103 | Thêm định nghĩa ranh giới car/van/truck, ngưỡng % cho `occluded_level`, quy tắc R-01…R-12, 27 ca khó | img_002, img_004, img_009, img_011, img_019, img_032 (cần chốt nhóm); các ca còn lại quyết theo quy tắc |
