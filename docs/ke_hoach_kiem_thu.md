# Kế hoạch kiểm thử DT041

Các ca dưới đây là kế hoạch cho đủ 4 tuần. Chỉ các ca validator và `can_place` có kết quả chạy trong tuần 1; không coi số `assert` là số ca độc lập.

| ID | Đối tượng | Input / mục tiêu | Expected | Tuần |
|---|---|---|---|---|
| T01 | Toàn chương trình | Ví dụ 1 trên phiếu | Nghiệm của phiếu | 2 |
| T02 | Toàn chương trình | Ví dụ 2 trên phiếu | Nghiệm của phiếu | 2 |
| T03 | Toàn chương trình | Bảng đầy hợp lệ | Giữ nguyên | 2 |
| T04 | Validator | Hai số 1 cùng hàng | Đề không hợp lệ | 1 |
| T05 | Validator | Ô bằng 5 | Đề không hợp lệ | 1 |
| T06 | Toàn chương trình | Toàn số 0 | Một nghiệm hợp lệ | 2 |
| T07 | Validator | Trùng riêng trong cột | Đề không hợp lệ | 1 |
| T08 | Validator | Trùng riêng trong khối 2×2 | Đề không hợp lệ | 1 |
| T09 | Validator | Thiếu hàng | Đề không hợp lệ | 1 |
| T10 | Validator | Một hàng chỉ có ba ô | Đề không hợp lệ | 1 |
| T11 | Validator | Ô bằng -1 | Đề không hợp lệ | 1 |
| T12 | Toàn chương trình | Chỉ một ô trống | Điền đúng một số | 2 |
| T13 | Toàn chương trình | Bảng hợp lệ buộc hoàn tác | Có nghiệm đúng, số hoàn tác > 0 | 3 |
| T14 | Toàn chương trình | Đề hợp lệ nhưng vô nghiệm | Không có nghiệm | 3 |
| T15 | `can_place` | Ô trống, giá trị hợp lệ và không hợp lệ | Boolean đúng; bảng không đổi | 1 |
| T16 | Bộ kiểm nghiệm | Bảng đầy sai | Từ chối | 2 |

T13–T14 sẽ được xây dựng và kiểm chứng độc lập trước khi điền kết quả. Mỗi ca hoàn thành phải có input đủ tái hiện, expected tính trước, actual, PASS/FAIL và log/ảnh/SHA tương ứng.
