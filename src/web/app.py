"""Màn hình thao tác Sudoku 4×4. Không chứa thuật toán giải riêng."""

from __future__ import annotations

from html import escape
from pathlib import Path

import streamlit as st

from src.terminal import EXAMPLES
from src.web.model import WebOutcome, evaluate

STYLE = Path(__file__).with_name("style.css")
EMPTY = [[0] * 4 for _ in range(4)]


def cell_key(row: int, col: int) -> str:
    return f"cell_{row}_{col}"


def load_board(board: list[list[int]]) -> None:
    for row in range(4):
        for col in range(4):
            value = board[row][col]
            st.session_state[cell_key(row, col)] = "" if value == 0 else str(value)
    st.session_state["outcome"] = None


def clear_outcome() -> None:
    st.session_state["outcome"] = None


def current_rows() -> list[list[str]]:
    return [[st.session_state[cell_key(row, col)] for col in range(4)] for row in range(4)]


def board_markup(outcome: WebOutcome) -> str:
    assert outcome.original is not None and outcome.result is not None
    assert outcome.result.board is not None
    parts = ['<div class="solution-grid" role="grid" aria-label="Bảng nghiệm Sudoku 4 nhân 4">']
    for row in range(4):
        for col in range(4):
            value = outcome.result.board[row][col]
            kind = "given" if outcome.original[row][col] else "filled"
            parts.append(
                f'<div role="gridcell" class="solution-cell {kind} row-{row} col-{col}" '
                f'aria-label="Hàng {row + 1} cột {col + 1}: {value}">{value}</div>'
            )
    parts.append("</div>")
    return "".join(parts)


def render_result(outcome: WebOutcome | None) -> None:
    st.markdown("### Kết quả")
    if outcome is None:
        st.markdown(
            '<div class="empty-state">Nhập đề hoặc nạp ví dụ, rồi chọn <strong>Giải bảng</strong>.</div>',
            unsafe_allow_html=True,
        )
        return

    status_label = {
        "invalid": "Đề không hợp lệ",
        "valid": "Đề hợp lệ",
        "unsolved": "Không có nghiệm",
        "solved": "Có nghiệm",
    }[outcome.status]
    st.markdown(
        f'<div class="status status-{outcome.status}"><span>{status_label}</span>'
        f'<p>{escape(outcome.message)}</p></div>',
        unsafe_allow_html=True,
    )

    if outcome.result is None:
        return
    result = outcome.result
    if result.board is not None:
        st.markdown("#### Nghiệm tìm được")
        st.markdown(board_markup(outcome), unsafe_allow_html=True)
        st.caption("Số cho trước giữ nguyên; số vừa điền được tô nhấn.")

    st.markdown(
        '<div class="run-stats">'
        f'<div><span>Lần thử</span><strong>{result.attempts}</strong></div>'
        f'<div><span>Lần đặt</span><strong>{result.placements}</strong></div>'
        f'<div><span>Hoàn tác</span><strong>{result.backtracks}</strong></div>'
        '</div>',
        unsafe_allow_html=True,
    )
    with st.expander(f"Xem vết chạy ({len(result.trace)} bước)"):
        if not result.trace:
            st.write("Đề đã đầy hoặc không cần đặt thêm số.")
        else:
            rows = [
                {
                    "Bước": index,
                    "Thao tác": event.action.capitalize(),
                    "Ô": f"({event.row + 1}, {event.col + 1})",
                    "Số": event.value,
                }
                for index, event in enumerate(result.trace, start=1)
            ]
            st.dataframe(rows, hide_index=True, width="stretch")


def main() -> None:
    st.set_page_config(page_title="Sudoku 4×4 · DT041", layout="wide", initial_sidebar_state="collapsed")
    st.markdown(f"<style>{STYLE.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    if cell_key(0, 0) not in st.session_state:
        load_board(EXAMPLES[1])

    st.markdown('<div class="project-mark">DT041 <span>·</span> Sudoku 4×4</div>', unsafe_allow_html=True)
    st.title("Giải Sudoku 4×4")
    st.write("Nhập số 1–4, để trống ô chưa biết. Bộ giải thử từng số và quay lui khi cần.")

    tools = st.columns([1, 1, 1, 3], gap="small", vertical_alignment="bottom")
    with tools[0]:
        st.button("Ví dụ 1", on_click=load_board, args=(EXAMPLES[1],), width="stretch")
    with tools[1]:
        st.button("Ví dụ 2", on_click=load_board, args=(EXAMPLES[2],), width="stretch")
    with tools[2]:
        st.button("Xóa bảng", on_click=load_board, args=(EMPTY,), width="stretch")

    left, right = st.columns([1, 1.1], gap="large")
    with left:
        st.markdown("### Bảng đề")
        st.caption("Bốn hàng, bốn cột; mỗi khối đậm gồm 2×2 ô.")
        with st.container(key="board_area"):
            for row in range(4):
                columns = st.columns(4, gap=None, wrap=False)
                for col, column in enumerate(columns):
                    with column:
                        st.text_input(
                            f"Hàng {row + 1}, cột {col + 1}",
                            key=cell_key(row, col),
                            max_chars=1,
                            label_visibility="collapsed",
                            on_change=clear_outcome,
                        )
        actions = st.columns([1, 1.4], gap="small")
        with actions[0]:
            if st.button("Kiểm tra đề", width="stretch"):
                st.session_state["outcome"] = evaluate(current_rows(), solve=False)
        with actions[1]:
            if st.button("Giải bảng", type="primary", width="stretch"):
                st.session_state["outcome"] = evaluate(current_rows(), solve=True)
        st.caption("Bảng nghiệm, thống kê và vết chạy đều lấy từ cùng bộ giải Python của bản terminal.")

    with right:
        render_result(st.session_state["outcome"])


if __name__ == "__main__":
    main()
