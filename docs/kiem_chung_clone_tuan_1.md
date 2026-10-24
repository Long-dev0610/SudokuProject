# Kiểm chứng từ clone sạch, tuần 1

- Repo: https://github.com/Long-dev0610/SudokuProject
- Commit mã C: `98d5cb426e223063acff1662301ebd86cec83364`
- Môi trường: Python 3.12.14 trên Windows.
- Thư mục kiểm chứng: `qa/repo_clone` nằm ngoài nội dung Git.

Các lệnh chạy từ thư mục gốc của bản clone:

```powershell
python -m unittest discover -s tests -q
python -m src.terminal --example 1
python -m src.terminal --example 2
```

Kết quả: 7 bài kiểm thử đều đạt. Cả hai ví dụ được terminal nhận là đề
hợp lệ. Chức năng giải quay lui chưa có trong tuần 1, do đó chưa khẳng định
kết quả nghiệm từ các lệnh này.
