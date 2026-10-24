# Định hướng giao diện Sudoku tuần 3

Nguồn hướng dẫn: `skills/design-taste-frontend/SKILL.md` và
`references/app-screens.md`. Sheet đã tạo bằng `scripts/draw.mjs --app`, lưu
trong `direction.json` với seed `1596326769` và style `framed-sheet`.

## Việc người dùng cần làm

Nhập hoặc nạp một bảng Sudoku 4×4, biết đề có hợp lệ không, giải một nghiệm,
và xem thuật toán đã thử và hoàn tác như thế nào. Câu hỏi chính của màn hình:
"Bảng này có giải được không, và thuật toán đã đi qua những bước nào?"

## Những thứ thuộc riêng sản phẩm

- Lưới 4×4 với bốn khối 2×2, có đường phân khối rõ ràng.
- Số 0 là ô trống; số cho trước và số chương trình điền cần phân biệt bằng
  trạng thái, không dựa riêng vào màu.
- Hai đề mẫu DT041 được nạp bằng một thao tác.
- Ba kết quả thật của lõi: đề sai, đề hợp lệ vô nghiệm, có nghiệm.
- Bước đặt và hoàn tác có tọa độ hàng/cột 1–4, đúng vết thuật toán.
- Số lần thử, số lần đặt, số lần hoàn tác phải lấy từ `SolveResult`.
- Bảng sau giải giữ nguyên số cho trước; bản gốc có thể xem lại.

## Hướng thể hiện

Dùng sheet `framed-sheet` làm điểm xuất phát: khung nền dịu, vùng làm việc
trắng, không đổ bóng; bảng Sudoku là phần lớn nhất và là nét nhận diện riêng.
Trên máy tính đặt lưới cạnh kết quả/vết chạy; trên điện thoại xếp dọc và giữ
ô đủ lớn để chạm. Một nút chính là "Giải bảng". Không dựng hero quảng cáo,
KPI giả, thẻ biểu tượng hàng loạt, gradient, glow hoặc số liệu bịa. Màu chỉ
nhấn trạng thái và ô đang xét; vẫn đọc được khi không phân biệt màu.

## Cổng kiểm tra trước khi giao

So sánh mọi kết quả web với terminal trên cùng input. Xem trạng thái rỗng,
đề sai, vô nghiệm, có nghiệm và lưới đầy. Chạy `lint.mjs --app` và
`inspect.mjs --app` tại 1440, 768 và 390 px sau khi có web; xem ảnh thực tế,
sửa ba vấn đề lớn nhất rồi kiểm tra lại. Chưa coi bước kiểm tra trình duyệt là
đã hoàn thành khi chưa có giao diện chạy thật.
