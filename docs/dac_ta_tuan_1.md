# Đặc tả DT041, tuần 1

Sinh viên Lê Minh Long, MSSV N24DCDT046, lớp D24CQDT01-N, Khoa Điện tử 2, ngành Kỹ thuật điện, điện tử. Phiếu: giải Sudoku thu nhỏ 4×4 bằng quay lui.

## Dữ liệu vào

Bảng `b` gồm đúng bốn hàng và mỗi hàng đúng bốn ô. Ô là số nguyên 0–4; 0 nghĩa là chưa điền. Các số khác 0 đã cho trước không được lặp trong hàng, cột hoặc khối 2×2. Terminal dùng tọa độ người dùng 1–4; phần lõi Python dùng 0–3.

## Dữ liệu ra của sản phẩm cuối

- Đề sai cấu trúc, miền giá trị hoặc có số cho trước xung đột: báo `ĐỀ KHÔNG HỢP LỆ` trước khi giải.
- Đề hợp lệ nhưng không có nghiệm: báo `KHÔNG CÓ NGHIỆM`.
- Có nghiệm: in một bảng đầy đủ, mỗi hàng/cột/khối chứa 1–4 đúng một lần, giữ nguyên các số đã cho. Không bắt buộc chứng minh nghiệm duy nhất.

Tuần 1 hiện chỉ hiện bảng, kiểm đề và kiểm một nước đặt. Hai trạng thái liên quan tìm kiếm thuộc tuần 2.

## Hai ví dụ trên phiếu

Ví dụ 1: `[[1,0,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,0]]`. Ví dụ 2: `[[0,2,3,4],[3,4,1,2],[2,1,0,3],[4,3,2,1]]`. Cả hai có kết quả theo phiếu: `[[1,2,3,4],[3,4,1,2],[2,1,4,3],[4,3,2,1]]`.

## Thiết kế thuật toán cuối

Sau khi kiểm đề, tìm ô 0 đầu tiên theo thứ tự hàng rồi cột. Thử `v=1..4`; chỉ đặt nếu `can_place` trả đúng. Gọi đệ quy cho phần còn lại. Nếu nhánh thất bại, hoàn tác ô về 0. Hết ô trống thì kiểm nghiệm và trả kết quả.

Gọi `z` là số ô trống. Cây thử thô có tối đa `4^z` lá; bảng 4×4 cố định làm cho mỗi lần kiểm hàng/cột/khối có chi phí hằng số. Bộ nhớ đệ quy `O(z)`. Đây là chặn lý thuyết của phần sẽ cài, chưa phải số đo thực nghiệm tuần 1.

Nguồn: giáo trình INT1306 chương 3, mục 3.6.2–3.6.3 và Bài 3.4; trang in 80–81, 84; trang PDF 92–93, 96. Phiếu DT041 trong bộ 91 phiếu giao đề.
