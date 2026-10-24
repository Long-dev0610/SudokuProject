# DT041 Sudoku 4×4

Kho GitHub: https://github.com/Long-dev0610/SudokuProject

Bài cá nhân của Lê Minh Long (N24DCDT046), Khoa Điện tử 2, ngành Kỹ thuật điện, điện tử; môn Cấu trúc dữ liệu và giải thuật INT13185, nhóm 03.

## Trạng thái tuần 3

Chương trình kiểm tra đề và giải Sudoku 4×4 bằng quay lui theo thứ tự hàng/cột. Hai ví dụ và năm ca bắt buộc trong phiếu DT041 đã đạt. Bản web Python dùng cùng `src/core/` với terminal; có nhập 16 ô, ví dụ, kiểm đề, giải, thống kê và vết chạy. Ca TK03 có nghiệm và thực sự đi qua 7 lần hoàn tác.

## Yêu cầu

Terminal: Python 3.10 trở lên, chỉ dùng thư viện chuẩn. Web: Python 3.11 trở lên và `streamlit==1.66.1` trong `requirements.txt`.

## Chạy terminal

Tại thư mục gốc dự án:

```powershell
python -m src.terminal --example 1
python -m src.terminal --example 2
python -m src.terminal --example 1 --trace
python -m src.terminal --input
python -m src.terminal --example 1 --check 1 2 2
python -m unittest discover -s tests -v
python -m scripts.test_catalog
python -m scripts.verify_oracle
```

Với `--input`, nhập bốn dòng, mỗi dòng gồm bốn số 0–4 cách nhau bằng khoảng trắng. `--check ROW COL VALUE` dùng chỉ số hàng/cột từ 1 đến 4 và kiểm số có thể đặt vào ô trống hay không.

Terminal in bảng nhập, thống kê số ứng viên đã thử, số lần đặt và số lần hoàn tác, sau đó in nghiệm. `--trace` in từng lần đặt/hoàn tác với tọa độ 1–4. Chương trình trả mã 0 khi có nghiệm, 1 khi đề hợp lệ nhưng vô nghiệm, 2 khi đề sai hoặc tham số không hợp lệ.

## Chạy web

Tại thư mục gốc dự án:

```powershell
python -m pip install -r requirements.txt
python -m streamlit run streamlit_app.py
```

Mở địa chỉ localhost do Streamlit in ra. Bản web và terminal chỉ khác giao diện; cả hai gọi `src/core/validation.py` và `src/core/solver.py`. Khi triển khai trên Streamlit Community Cloud, chọn repo này, nhánh `main`, tệp khởi chạy `streamlit_app.py`, và Python 3.11 trở lên. URL triển khai sẽ bổ sung sau khi tạo ứng dụng trên tài khoản của sinh viên.

Ca TK03 kiểm nhánh quay lui có nghiệm (nhập bằng `--input` hoặc trên web):

```text
1 0 0 4
0 0 1 0
0 4 0 0
3 0 0 0
```

Nghiệm đúng là `1 3 2 4 / 4 2 1 3 / 2 4 3 1 / 3 1 4 2`; bộ giải ghi 55 lần thử, 18 lần đặt, 7 lần hoàn tác.

## Quy tắc

`0` là ô trống. Số cho trước phải thuộc 1–4 và không trùng trong hàng, cột hay khối 2×2. Bảng có số cho trước xung đột bị từ chối trước khi tìm kiếm. Đề hợp lệ nhưng không giải được có trạng thái riêng. Bộ giải không sửa bảng đầu vào; nghiệm giữ nguyên các số cho trước. Không yêu cầu nghiệm duy nhất.

## Cấu trúc

- `src/core/validation.py`: lõi kiểm tra đề và nước đặt, dùng chung cho terminal và web.
- `src/core/solver.py`: quay lui, kiểm nghiệm cuối, thống kê và vết đặt/hoàn tác.
- `src/terminal.py`: giao diện dòng lệnh.
- `tests/`: kiểm thử tự động.
- `src/web/`: lớp chuyển dữ liệu và giao diện Streamlit; `streamlit_app.py` là điểm chạy.
- `scripts/test_catalog.py`: expected/actual/PASS của 16 ca độc lập.
- `scripts/verify_oracle.py`: liệt kê nghiệm 4×4 độc lập để kiểm tra hai ví dụ và ca vô nghiệm.
- `docs/logs/`: stdout của các lệnh đã chạy trên commit C.
- `docs/anh_ket_qua/`: 11 ảnh minh chứng cá nhân từ tuần 2. Ảnh bổ sung tuần 3 được ghi rõ phiên bản khi có.

Tài liệu soạn báo cáo và công cụ tạo DOCX/PDF được giữ ngoài kho mã/GitHub;
chúng không phải thành phần cần thiết để chạy chương trình.

Thông tin gốc: phiếu DT041 trong `91_Phieu_giao_de_tai_INT13185_N03.docx`, giáo trình INT1306 chương 3 mục 3.6.2–3.6.3 và Bài 3.4.
