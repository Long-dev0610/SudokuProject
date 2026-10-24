"""Cập nhật thông tin cá nhân của bản nộp tuần 1."""

from pathlib import Path

root = Path(__file__).resolve().parents[1]
path = root / "nop_tuan_01" / "N24DCDT046_DT041_LeMinhLong_ThongTinNop.txt"
text = path.read_text(encoding="utf-8")
text = text.replace(
    "Lớp: D24CQDT01-N\n",
    "Lớp: D24CQDT01-N\nKhoa: Điện tử 2\nNgành: Kỹ thuật điện, điện tử\n",
)
path.write_text(text, encoding="utf-8")
