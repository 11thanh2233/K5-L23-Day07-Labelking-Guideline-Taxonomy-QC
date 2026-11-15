# Tóm tắt QC (nhớ nhanh)

## Đơn vị và ngưỡng

| Đại lượng | Công thức / quy tắc | Ngưỡng |
|---|---|---|
| IoU | giao / hợp của hai box | box cao ≥ 50 px: ≥ 0.85; cao 20–50 px: ≥ 0.7 |
| IAA (hai người gán độc lập) | IoU trung bình trên các cặp box ghép được; % cùng lớp | IoU TB ≥ 0.85 và cùng lớp ≥ 95% |
| Tỉ lệ lỗi theo **đối tượng** | đối tượng lỗi / đối tượng trong mẫu | (báo cáo kèm mẫu số) |
| Tỉ lệ lỗi theo **ảnh** | ảnh có ≥ 1 lỗi / ảnh trong mẫu | **≤ 2%** mới được Release |
| Vật quá nhỏ | cao < 20 px | không gán từng vật, vẽ `ignore_region` |
| Cỡ mẫu QC (lô lớn) | ngẫu nhiên, ≥ 10% và tối thiểu 50 ảnh, cộng mọi ảnh ca khó | lô < 500 ảnh: kiểm 100% |

Trong lab, lô chỉ có 40 ảnh nên script lấy mẫu = mọi ảnh từng bị cờ + 20 ảnh ngẫu nhiên (nới lỏng để vừa thời gian). Báo cáo phải nói rõ mẫu.

Luôn ghi **mẫu số**: "6/40 ảnh = 15%" chứ không chỉ "15%".

## Năm loại lỗi (mọi lỗi thuộc đúng một loại)

| Mã trong `qc_review.csv` | Loại | Ví dụ |
|---|---|---|
| `bo_sot` | Bỏ sót | xe có thật mà không có box |
| `thua` | Thừa | box trên xe phản chiếu / tượng / hình in |
| `sai_lop` | Sai lớp | xe con gán `truck` |
| `sai_vi_tri_kich_thuoc` | Sai vị trí, kích thước | box lỏng, thiếu đuôi xe |
| `sai_thuoc_tinh` | Sai thuộc tính | `occluded_level` sai mức |
| `khong` | Không lỗi | ảnh đã kiểm, sạch |

## Cây quyết định: Hold → Rework → Release

1. Guideline chưa rõ hoặc dữ liệu hỏng? → **Hold** (làm rõ rồi quay lại).
2. > 2% ảnh có lỗi, **hoặc lỗi lặp lại cùng một kiểu**, hoặc IoU / IAA dưới ngưỡng? → **Rework** (sửa rồi kiểm lại).
3. Còn lại → **Release**, kèm báo cáo QC.

Lỗi ít nhưng lặp lại một kiểu vẫn là Rework: đó là lỗi hệ thống.

## Calibration: mỗi quyết định một dòng

| Ca | Quyết định | Phiên bản |
|---|---|---|
| Xe bị cột che 60% | `occluded_level = 2` | v1.1 |

IAA thấp thì sửa guideline hay sửa người? Cả hai lệch cùng loại ca → quy tắc mơ hồ, **sửa guideline**.
Chỉ một người lệch → người đó chưa nắm quy tắc, **hướng dẫn lại**. Giống nhau nhưng cùng sai → cùng hiểu sai, **đối chiếu guideline / gold**.
