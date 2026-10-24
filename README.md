# DT041 Sudoku 4×4

Kho GitHub: https://github.com/Long-dev0610/SudokuProject

Bài cá nhân của Lê Minh Long (N24DCDT046), Khoa Điện tử 2, ngành Kỹ thuật điện, điện tử; môn Cấu trúc dữ liệu và giải thuật INT13185, nhóm 03.

## Trạng thái tuần 1

Chương trình Python hiện kiểm tra cấu trúc bảng, miền giá trị, các số cho trước trong hàng, cột và khối 2×2. Hàm `can_place` kiểm một nước đặt mà không sửa bảng. Bộ giải quay lui và giao diện web thuộc các tuần tiếp theo.

## Yêu cầu

Python 3.10 trở lên; chỉ dùng thư viện chuẩn. Không cần cài gói ngoài.

## Chạy terminal

Tại thư mục gốc dự án:

```powershell
python -m src.terminal --example 1
python -m src.terminal --example 2
python -m src.terminal --input
python -m src.terminal --example 1 --check 1 2 2
python -m unittest discover -s tests -v
```

Với `--input`, nhập bốn dòng, mỗi dòng gồm bốn số 0–4 cách nhau bằng khoảng trắng. `--check ROW COL VALUE` dùng chỉ số hàng/cột từ 1 đến 4 và kiểm số có thể đặt vào ô trống hay không.

Terminal hiện chỉ báo tính hợp lệ của đề và khả năng đặt số. Không in nghiệm cho đến khi bộ giải được cài ở tuần 2.

## Quy tắc

`0` là ô trống. Số cho trước phải thuộc 1–4 và không trùng trong hàng, cột hay khối 2×2. Bảng có số cho trước xung đột bị từ chối trước khi tìm kiếm. Một đề hợp lệ vẫn có thể vô nghiệm; tuần 2 sẽ bổ sung trạng thái này.

## Cấu trúc

- `src/core/validation.py`: lõi kiểm tra đề và nước đặt, dùng chung cho terminal và web khi web được triển khai.
- `src/terminal.py`: giao diện dòng lệnh.
- `tests/`: kiểm thử tự động.
- `docs/logs/`: stdout của các lệnh đã chạy trên commit C.
- `docs/anh_ket_qua/`: ảnh minh chứng cá nhân sẽ bổ sung theo tiến độ.

Tài liệu soạn báo cáo và công cụ tạo DOCX/PDF được giữ ngoài kho mã/GitHub;
chúng không phải thành phần cần thiết để chạy chương trình.

Thông tin gốc: phiếu DT041 trong `91_Phieu_giao_de_tai_INT13185_N03.docx`, giáo trình INT1306 chương 3 mục 3.6.2–3.6.3 và Bài 3.4.
