"""Màn hình thao tác Sudoku 4×4. Không chứa thuật toán giải riêng."""

from __future__ import annotations

from html import escape
from pathlib import Path
from time import monotonic

import streamlit as st

from src.web.model import TraceFrame, WebOutcome, evaluate, frame_at
from src.web.puzzles import random_puzzle

STYLE = Path(__file__).with_name("style.css")
EMPTY = [[0] * 4 for _ in range(4)]
BACKTRACK_DEMO = [[1, 0, 0, 4], [0, 0, 1, 0], [0, 4, 0, 0], [3, 0, 0, 0]]


def cell_key(row: int, col: int) -> str:
    return f"cell_{row}_{col}"


def load_board(board: list[list[int]]) -> None:
    for row in range(4):
        for col in range(4):
            value = board[row][col]
            st.session_state[cell_key(row, col)] = "" if value == 0 else str(value)
    st.session_state["outcome"] = None
    st.session_state["trace_step"] = 0
    st.session_state["autoplay"] = False


def load_random_board() -> None:
    previous = current_rows()
    for _ in range(10):
        board = random_puzzle()
        if [["" if value == 0 else str(value) for value in row] for row in board] != previous:
            break
    load_board(board)


def clear_outcome() -> None:
    st.session_state["outcome"] = None
    st.session_state["trace_step"] = 0
    st.session_state["autoplay"] = False


def current_rows() -> list[list[str]]:
    return [[st.session_state[cell_key(row, col)] for col in range(4)] for row in range(4)]


def render_result(outcome: WebOutcome | None) -> None:
    st.markdown(
        '<div class="section-head"><span class="section-index">02</span>'
        '<div><h2>Kết quả</h2><p>Nghiệm và vết chạy của bộ giải quay lui.</p></div></div>',
        unsafe_allow_html=True,
    )
    if outcome is None:
        st.markdown(
            '<div class="empty-state"><span class="empty-kicker">Cách thuật toán hoạt động</span>'
            '<strong>Từ ô trống đầu tiên đến nghiệm</strong>'
            '<ol><li>Chọn ô trống theo hàng rồi cột.</li>'
            '<li>Thử 1–4 và kiểm hàng, cột, khối 2×2.</li>'
            '<li>Đặt số hợp lệ; nếu nhánh thất bại, trả ô về 0.</li></ol>'
            '<p>Chọn “Xem thuật toán giải” để quan sát từng bước thật.</p></div>',
            unsafe_allow_html=True,
        )
        return

    status_label = "Đề không hợp lệ" if outcome.status == "invalid" else "Đề hợp lệ"
    st.markdown(
        f'<div class="status status-{outcome.status}"><span>{status_label}</span>'
        f'<p>{escape(outcome.message)}</p></div>',
        unsafe_allow_html=True,
    )

def trace_board_markup(outcome: WebOutcome, frame: TraceFrame) -> str:
    assert outcome.original is not None
    event = frame.event
    parts = ['<div class="trace-grid" role="grid" aria-label="Bảng Sudoku tại bước hiện tại">']
    for row in range(4):
        for col in range(4):
            value = frame.board[row][col]
            classes = ["trace-cell", f"row-{row}", f"col-{col}"]
            if outcome.original[row][col]:
                classes.append("given")
            elif value:
                classes.append("filled")
            if event and event.row == row and event.col == col:
                classes.append("active")
                if event.action == "thử" and event.conflicts:
                    classes.append("rejected")
                if event.action == "hoàn tác":
                    classes.append("undone")
            trial = bool(event and event.action == "thử" and event.row == row and event.col == col and not value)
            shown = f'<span class="trial-value">{event.value}</span>' if trial else (
                str(value) if value else '<span aria-hidden="true">·</span>'
            )
            label = f"Hàng {row + 1}, cột {col + 1}: " + (
                f"đang thử {event.value}, chưa đặt" if trial else str(value) if value else "trống"
            )
            parts.append(f'<div role="gridcell" class="{" ".join(classes)}" aria-label="{label}">{shown}</div>')
    parts.append("</div>")
    return "".join(parts)


def describe_step(frame: TraceFrame, total: int, step: int, solved: bool) -> tuple[str, str, str]:
    event = frame.event
    if total == 0 and solved:
        return "Bảng đã hoàn chỉnh", "Đề ban đầu đã là một nghiệm hợp lệ; thuật toán không cần thử hay đặt thêm số.", "done"
    if step == total and not solved:
        return "Không có nghiệm", "Mọi nhánh đã được thử và hoàn tác; không có cách điền hợp lệ cho đề này.", "undo"
    if event is None:
        return "Bảng ban đầu", "Bộ giải sẽ tìm ô trống đầu tiên theo hàng rồi cột.", "start"
    position = f"hàng {event.row + 1}, cột {event.col + 1}"
    if event.action == "chọn":
        return "Chọn ô trống", f"Ô trống đầu tiên là {position}. Bắt đầu thử các số từ 1 đến 4.", "select"
    if event.action == "thử":
        if event.conflicts:
            labels = {"row": "hàng", "column": "cột", "block": "khối 2×2", "occupied": "ô đã có số"}
            reason = ", ".join(labels[code] for code in event.conflicts)
            return "Loại số vừa thử", f"Thử {event.value} tại {position}: trùng trong {reason}. Bảng chưa thay đổi.", "reject"
        return "Số thỏa ràng buộc", f"Thử {event.value} tại {position}: không trùng trong hàng, cột hoặc khối 2×2.", "accept"
    if event.action == "hoàn tác":
        return "Quay lui · trả ô về 0", f"Nhánh bắt đầu bằng {event.value} tại {position} không dẫn đến nghiệm. Xóa số và thử hướng khác.", "undo"
    if step == total:
        return ("Tìm thấy nghiệm" if solved else "Đã duyệt hết nhánh"), (
            "Mọi ô đã được điền hợp lệ; các số cho trước giữ nguyên." if solved
            else "Không còn số hợp lệ để thử; đề này không có nghiệm."
        ), ("done" if solved else "undo")
    return "Đặt số và đi sâu", f"Đặt {event.value} vào {position}, rồi tiếp tục tìm ô trống kế tiếp.", "place"


def change_step(delta: int, total: int) -> None:
    st.session_state["autoplay"] = False
    st.session_state["trace_step"] = max(0, min(total, st.session_state.get("trace_step", 0) + delta))


def jump_step(step: int) -> None:
    st.session_state["autoplay"] = False
    st.session_state["trace_step"] = step


def toggle_autoplay(total: int) -> None:
    if st.session_state.get("autoplay"):
        st.session_state["autoplay"] = False
    elif total:
        if st.session_state.get("trace_step", 0) >= total:
            st.session_state["trace_step"] = 0
        st.session_state["autoplay"] = True
        st.session_state["auto_tick"] = monotonic()


def advance_autoplay(total: int) -> None:
    if not st.session_state.get("autoplay"):
        return
    now = monotonic()
    if now - st.session_state.get("auto_tick", now) < 0.55:
        return
    st.session_state["trace_step"] = min(total, st.session_state.get("trace_step", 0) + 1)
    st.session_state["auto_tick"] = now
    if st.session_state["trace_step"] >= total:
        st.session_state["autoplay"] = False


def pseudocode_for(action: str | None, *, finished: bool, solved: bool) -> str:
    if finished:
        return "return True  # có nghiệm" if solved else "return False  # không có nghiệm"
    return {
        None: "giai_sudoku(b)",
        "chọn": "r, c = o_trong_dau_tien(b)",
        "thử": "for v in 1..4: kiem_tra_hang_cot_khoi(b, r, c, v)",
        "đặt": "b[r][c] = v; giai_sudoku(b)",
        "hoàn tác": "b[r][c] = 0",
    }[action]


@st.fragment(run_every="0.6s")
def render_walkthrough(outcome: WebOutcome) -> None:
    assert outcome.original is not None and outcome.result is not None
    result = outcome.result
    total = len(result.trace)
    advance_autoplay(total)
    step = min(st.session_state.get("trace_step", 0), total)
    st.session_state["trace_step"] = step

    st.markdown('<div class="walkthrough-kicker">Quay lui theo thứ tự hàng → cột</div>', unsafe_allow_html=True)
    st.title("Theo dõi từng bước giải")
    st.markdown('<p class="intro">Mỗi bước dưới đây được ghi khi bộ giải Python thực sự chạy; bảng có thể tua lại mà không tính lại nghiệm.</p>', unsafe_allow_html=True)

    with st.container(key="walkthrough"):
        st.markdown(f'<div class="progress-label">Bước <strong>{step}</strong> / {total}</div>', unsafe_allow_html=True)
        with st.container(key="trace_controls"):
            controls = st.columns([1, 1, 1, 1], gap="small")
            with controls[0]:
                st.button("Về đầu", on_click=jump_step, args=(0,), disabled=step == 0, width="stretch")
            with controls[1]:
                st.button("Bước trước", on_click=change_step, args=(-1, total), disabled=step == 0, width="stretch")
            with controls[2]:
                st.button("Bước tiếp", on_click=change_step, args=(1, total), disabled=step == total, type="primary", width="stretch")
            with controls[3]:
                st.button("Xem kết quả", on_click=jump_step, args=(total,), disabled=step == total, width="stretch")
        if total:
            st.slider("Chọn bước để xem", min_value=0, max_value=total, key="trace_step")
            with st.container(key="playback_controls"):
                play_col, note_col = st.columns([1, 2], gap="small")
                with play_col:
                    st.button(
                        "Tạm dừng" if st.session_state.get("autoplay") else "Chạy tự động",
                        on_click=toggle_autoplay, args=(total,), width="stretch",
                    )
                with note_col:
                    st.caption("Tự chuyển từng bước; có thể tạm dừng hoặc tua thủ công.")
        else:
            st.caption("Bảng đã đầy; không có bước thử để tua.")

        frame = frame_at(outcome, step)
        board_col, detail_col = st.columns([1, 1], gap="large")
        with board_col:
            st.markdown('<div class="trace-section-label">Trạng thái bảng</div>', unsafe_allow_html=True)
            st.markdown(trace_board_markup(outcome, frame), unsafe_allow_html=True)
            st.markdown('<p class="trace-legend">Số đen: đề cho trước · Số xanh: thuật toán đã đặt · Ô viền: bước hiện tại</p>', unsafe_allow_html=True)
        with detail_col:
            title, message, kind = describe_step(frame, total, step, result.board is not None)
            st.markdown('<div class="trace-section-label">Điều gì đang xảy ra?</div>', unsafe_allow_html=True)
            st.markdown(
                f'<div class="step-card step-{kind}"><span class="step-number">{step:02d} / {total:02d}</span>'
                f'<h2>{escape(title)}</h2><p>{escape(message)}</p></div>',
                unsafe_allow_html=True,
            )
            pseudocode = pseudocode_for(
                frame.event.action if frame.event else None,
                finished=step == total, solved=result.board is not None,
            )
            st.markdown(
                '<div class="pseudo-line"><span>Dòng tương ứng trong giả mã</span>'
                f'<code>{escape(pseudocode)}</code></div>',
                unsafe_allow_html=True,
            )
            if frame.event and frame.event.action == "thử":
                checks = [("Hàng", "row"), ("Cột", "column"), ("Khối 2×2", "block")]
                badges = "".join(
                    f'<div class="constraint {"fail" if code in frame.event.conflicts else "pass"}">'
                    f'<span>{escape(label)}</span><strong>{"Trùng" if code in frame.event.conflicts else "Đạt"}</strong></div>'
                    for label, code in checks
                )
                st.markdown(f'<div class="constraints">{badges}</div>', unsafe_allow_html=True)
            st.markdown(
                '<div class="run-stats">'
                f'<div><span>Số đã thử</span><strong>{frame.attempts} / {result.attempts}</strong></div>'
                f'<div><span>Lần đặt</span><strong>{frame.placements} / {result.placements}</strong></div>'
                f'<div><span>Hoàn tác</span><strong>{frame.backtracks} / {result.backtracks}</strong></div>'
                '</div>',
                unsafe_allow_html=True,
            )
            if step == total:
                final = "Có nghiệm" if result.board is not None else "Không có nghiệm"
                st.markdown(f'<div class="final-state">Kết luận: <strong>{final}</strong></div>', unsafe_allow_html=True)

    with st.expander(f"Xem danh sách {total} bước"):
        if not result.trace:
            st.write("Bảng đã đầy; không có bước thử nào.")
        else:
            rows = []
            for index, event in enumerate(result.trace, 1):
                verdict = ""
                if event.action == "thử":
                    labels = {"row": "hàng", "column": "cột", "block": "khối", "occupied": "ô đã có số"}
                    verdict = "Loại: " + ", ".join(labels[code] for code in event.conflicts) if event.conflicts else "Đạt"
                rows.append({"Bước": index, "Thao tác": event.action.capitalize(),
                             "Ô": f"({event.row + 1}, {event.col + 1})", "Số": str(event.value) if event.value else "—", "Kiểm tra": verdict})
            st.dataframe(rows, hide_index=True, width="stretch")


def render_input_controls() -> None:
    st.markdown(
        '<div class="section-head"><span class="section-index">01</span>'
        '<div><h2>Bảng đề</h2><p>Mỗi khối viền đậm gồm 2×2 ô.</p></div></div>',
        unsafe_allow_html=True,
    )
    with st.container(key="example_tools"):
        tools = st.columns(2, gap="small")
        with tools[0]:
            st.button("Đề ngẫu nhiên", on_click=load_random_board, width="stretch")
        with tools[1]:
            st.button("Ca quay lui", on_click=load_board, args=(BACKTRACK_DEMO,), width="stretch")
    st.markdown('<p class="board-note">Tự tạo đề: điền số 1–4 vào ô cho trước; để trống ô chưa biết. Đề ngẫu nhiên có 11 ô trống và một nghiệm.</p>', unsafe_allow_html=True)
    with st.container(key="board_area"):
        for row in range(4):
            columns = st.columns(4, gap=None, wrap=False)
            for col, column in enumerate(columns):
                with column:
                    st.text_input(
                        f"Hàng {row + 1}, cột {col + 1}", key=cell_key(row, col),
                        max_chars=1, label_visibility="collapsed", on_change=clear_outcome,
                    )
    with st.container(key="action_tools"):
        actions = st.columns([1, 1.5, .8], gap="small")
        with actions[0]:
            if st.button("Kiểm tra đề", width="stretch"):
                st.session_state["outcome"] = evaluate(current_rows(), solve=False)
                st.rerun()
        with actions[1]:
            if st.button("Xem thuật toán giải", type="primary", width="stretch"):
                st.session_state["outcome"] = evaluate(current_rows(), solve=True)
                st.session_state["trace_step"] = 0
                st.rerun()
        with actions[2]:
            st.button("Xóa", on_click=load_board, args=(EMPTY,), width="stretch")
    st.markdown('<p class="board-note">Số đã cho được giữ nguyên khi giải.</p>', unsafe_allow_html=True)


def main() -> None:
    st.set_page_config(page_title="Sudoku 4×4 · DT041", layout="wide", initial_sidebar_state="collapsed")
    st.markdown(f"<style>{STYLE.read_text(encoding='utf-8')}</style>", unsafe_allow_html=True)
    if cell_key(0, 0) not in st.session_state:
        load_board(EMPTY)

    st.markdown('<div class="project-mark"><span class="project-symbol">4×4</span><span>DT041 · Sudoku 4×4</span></div>', unsafe_allow_html=True)
    outcome = st.session_state["outcome"]
    if outcome is not None and outcome.result is not None:
        render_walkthrough(outcome)
        with st.expander("Đổi đề hoặc nhập bảng khác"):
            render_input_controls()
    else:
        st.title("Giải Sudoku 4×4")
        st.markdown('<p class="intro">Tạo một đề ngẫu nhiên hoặc tự nhập các số cho trước để theo dõi cách thuật toán giải.</p>', unsafe_allow_html=True)
        with st.container(key="workbench"):
            left, right = st.columns([1, 1], gap="large")
            with left:
                render_input_controls()
            with right:
                with st.container(key="result_panel"):
                    render_result(outcome)
    st.markdown('<p class="page-foot">Bản web dùng cùng thuật toán Python với chương trình terminal.</p>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()
