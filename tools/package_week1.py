"""Đóng gói mã tuần 1, bỏ nguồn giảng viên và tệp tạm."""

from pathlib import Path
from zipfile import ZIP_DEFLATED, ZipFile

ROOT = Path(__file__).resolve().parents[1]
OUT = ROOT / "nop_tuan_01" / "N24DCDT046_DT041_LeMinhLong_MaNguon.zip"
INCLUDE = [ROOT / "README.md", ROOT / ".gitignore"]
for folder in ("src", "tests", "docs"):
    INCLUDE.extend(
        path for path in (ROOT / folder).rglob("*")
        if path.is_file() and "__pycache__" not in path.parts and path.suffix != ".pyc"
    )

OUT.parent.mkdir(parents=True, exist_ok=True)
with ZipFile(OUT, "w", compression=ZIP_DEFLATED) as package:
    for path in sorted(INCLUDE):
        package.write(path, path.relative_to(ROOT))
print(OUT)
