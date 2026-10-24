"""Xuất bản PDF nội dung từ DOCX bằng ReportLab khi máy không có LibreOffice."""

from __future__ import annotations

from html import escape
from pathlib import Path

from docx import Document
from docx.oxml.ns import qn
from docx.table import Table as WordTable
from docx.text.paragraph import Paragraph as WordParagraph
from reportlab.lib import colors
from reportlab.lib.enums import TA_CENTER, TA_LEFT
from reportlab.lib.pagesizes import A4
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.units import cm
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.platypus import BaseDocTemplate, Frame, LongTable, PageBreak, PageTemplate, Paragraph, Spacer, TableStyle


ROOT = Path(__file__).resolve().parents[1]
DOCX = ROOT / "nop_tuan_01" / "N24DCDT046_DT041_LeMinhLong_BaoCao.docx"
PDF = DOCX.with_suffix(".pdf")

pdfmetrics.registerFont(TTFont("TimesVN", r"C:\Windows\Fonts\times.ttf"))
pdfmetrics.registerFont(TTFont("TimesVN-Bold", r"C:\Windows\Fonts\timesbd.ttf"))
pdfmetrics.registerFontFamily("TimesVN", normal="TimesVN", bold="TimesVN-Bold")

normal = ParagraphStyle("normal", fontName="TimesVN", fontSize=11, leading=16, spaceAfter=5)
h1 = ParagraphStyle("h1", parent=normal, fontName="TimesVN-Bold", fontSize=15, leading=19, spaceBefore=16, spaceAfter=8)
h2 = ParagraphStyle("h2", parent=normal, fontName="TimesVN-Bold", fontSize=12, leading=17, spaceBefore=11, spaceAfter=5)
h3 = ParagraphStyle("h3", parent=normal, fontName="TimesVN-Bold", fontSize=11, leading=16, spaceBefore=8, spaceAfter=4)
center = ParagraphStyle("center", parent=normal, alignment=TA_CENTER)
table_style = ParagraphStyle("table", parent=normal, fontSize=9, leading=12, spaceAfter=0)


def ptext(text: str, style=normal):
    return Paragraph(escape(text).replace("\n", "<br/>"), style)


def footer(canvas, doc):
    canvas.saveState()
    canvas.setFont("TimesVN", 9)
    canvas.drawRightString(A4[0] - 2 * cm, 1.3 * cm, str(doc.page))
    canvas.restoreState()


def main():
    source = Document(DOCX)
    doc = BaseDocTemplate(
        str(PDF), pagesize=A4, leftMargin=3 * cm, rightMargin=2 * cm,
        topMargin=2 * cm, bottomMargin=2 * cm,
        title="Báo cáo tiến độ tuần 1 DT041 Sudoku 4×4",
        author="Lê Minh Long",
    )
    frame = Frame(doc.leftMargin, doc.bottomMargin, doc.width, doc.height, id="normal")
    doc.addPageTemplates(PageTemplate(id="page", frames=[frame], onPage=footer))
    story = []
    cover_title_count = 0
    for child in source.element.body.iterchildren():
        if child.tag == qn("w:p"):
            item = WordParagraph(child, source._body)
            txt = item.text.strip()
            if not txt:
                continue
            if txt == "BỘ KHOA HỌC VÀ CÔNG NGHỆ":
                cover_title_count += 1
                if cover_title_count == 2:
                    story.append(PageBreak())
            style_name = item.style.name.lower()
            if "heading 1" in style_name or txt.startswith("CHƯƠNG "):
                style = h1
            elif "heading 2" in style_name:
                style = h2
            elif "heading 3" in style_name:
                style = h3
            elif item.alignment == 1:
                style = center
            else:
                style = normal
            story.append(ptext(txt, style))
        elif child.tag == qn("w:tbl"):
            table = WordTable(child, source._body)
            data = []
            for row in table.rows:
                cells = [ptext(cell.text.strip() or " ", table_style) for cell in row.cells]
                if any(cell.text.strip() for cell in row.cells):
                    data.append(cells)
            if not data:
                continue
            width = doc.width / len(data[0])
            rendered = LongTable(data, colWidths=[width] * len(data[0]), repeatRows=1, hAlign="LEFT")
            rendered.setStyle(TableStyle([
                ("GRID", (0, 0), (-1, -1), 0.35, colors.HexColor("#D9D9D9")),
                ("BACKGROUND", (0, 0), (-1, 0), colors.HexColor("#E9EDF2")),
                ("VALIGN", (0, 0), (-1, -1), "MIDDLE"),
                ("LEFTPADDING", (0, 0), (-1, -1), 5),
                ("RIGHTPADDING", (0, 0), (-1, -1), 5),
                ("TOPPADDING", (0, 0), (-1, -1), 5),
                ("BOTTOMPADDING", (0, 0), (-1, -1), 5),
            ]))
            story.extend([Spacer(1, 5), rendered, Spacer(1, 9)])
    doc.build(story)
    print(PDF)


if __name__ == "__main__":
    main()
