# Tóm tắt IAA (taxonomy v0)

- Ảnh được so sánh (có >=2 người gán): **40**; số người gán: 3
- Lượt gán đủ **80/80**.
- IoU trung bình và % cùng lớp **chỉ tính trên các cặp box đã ghép** (IoU >= 0.5, ghép 1-1 không phân biệt lớp). Box chưa ghép được thống kê riêng ở cột bỏ sót/thừa.
- Mẫu số: 303 cặp box ghép (tổng mọi cặp người gán, ảnh chung).

| Cặp | Ảnh | Cặp box ghép | IoU TB | Cùng lớp | Cùng occluded_level | Cùng truncated | Chưa ghép (A/B) | Bỏ qua do ignore | Đạt IAA |
|---|---|---|---|---|---|---|---|---|---|
| **TỔNG** | 40 | 303 | 0.818 | 94.1% | 45.5% | 58.4% | 54/117 | 0 | CHƯA ĐẠT |
| 101|102 | 13 | 117 | 0.814 | 89.7% | 36.8% | 32.5% | 33/20 | 0 | CHƯA ĐẠT |
| 101|103 | 13 | 119 | 0.817 | 97.5% | 58.8% | 95.0% | 18/76 | 0 | CHƯA ĐẠT |
| 102|103 | 14 | 67 | 0.828 | 95.5% | 37.3% | 38.8% | 3/21 | 0 | CHƯA ĐẠT |

Ngưỡng IAA: IoU TB >= 0.85, đồng thuận lớp >= 95%.

Số ca bất thường: 648 ({'bo_sot_thua': 107, 'iou_thap': 129, 'sai_thuoc_tinh': 200, 'co_can_review': 36, 'bat_dong_ignore': 150, 'sai_lop': 18, 'can_review_anh': 8}), trên 37 ảnh cần calibration.
