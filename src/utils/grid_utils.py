import tkinter as tk
import tkinter.ttk as ttk

from src.config import DEFAULT_PADY

next_frame_rows = {}


def add(
    master: tk.Misc,
    widget: ttk.Widget | tk.Widget,
    column: int,
    pady: int = DEFAULT_PADY,
    **grid_kwargs,
):
    """
    Allow rows to grow automatically.
    """
    frame_id = id(master)

    if frame_id not in next_frame_rows:
        next_frame_rows[frame_id] = {}

    if column not in next_frame_rows[frame_id]:
        next_frame_rows[frame_id][column] = 0

    current_row = next_frame_rows[frame_id][column]

    widget.grid(row=current_row, column=column, pady=pady, **grid_kwargs)

    next_frame_rows[frame_id][column] += 1


def get_current_row(master: tk.Misc, column: int):
    frame_id = id(master)

    if frame_id not in next_frame_rows:
        return 0

    if column not in next_frame_rows[frame_id]:
        return 0

    return next_frame_rows[frame_id][column]


def reset():
    next_frame_rows.clear()
