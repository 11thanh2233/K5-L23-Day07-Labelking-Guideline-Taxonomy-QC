# Thông tin nhóm

- Tên nhóm: Labelking
- Mã thành viên (ba chữ số): 101 (2A202603211), 102(2A202603033), 103 (2A202603118)
- Người điều phối: Võ Duy Thành (101)
- Người review bản cuối: Bùi Anh Dũng (102)
- Commit chốt bài (điền ở kênh nộp sau khi commit): Lab07_Nopbai

## Kết quả tóm tắt (điền cuối bài)

- Lượt gán hoàn tất / được giao: 80/80 (40 ảnh × 2 người; 101: 26 ảnh, 102: 27, 103: 27)
- IAA trước calibration (kèm mẫu số): IoU TB 0.818 và cùng lớp 94.1% (285/303) trên 303 cặp box ghép — chưa đạt ngưỡng 0.85 / 95%
- Số ảnh phải calibration: 37 / 40 (648 ca); do đổi guideline `semantic` và taxonomy v1.1 nên rà lại cả 40 / 40
- Vòng QC và số ảnh đã duyệt / cả lô: vòng 1: 40/40 (Rework); vòng 2: 40/40
- Tỉ lệ lỗi: vòng 2: 0.0 % theo ảnh (0/40), 0.0 % theo đối tượng (0/473); vòng 1: 30.0 % theo ảnh (12/40), 3.1 % theo đối tượng (15/480)
- **Quyết định** (Release / Hold / Rework) và lý do một dòng: Release — vòng 1 Rework (30% ảnh lỗi > 2%), sửa 19 ca Q01–Q19 rồi vòng 2 đạt 0/40 ảnh lỗi; nhãn calibration sinh bằng script và phiếu QC điền với hỗ trợ AI, 103 cần xác nhận (xem QC_REPORT.md)
