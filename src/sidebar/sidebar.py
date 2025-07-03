# Original author: Olikonsti
# Modified from: https://github.com/Olikonsti/TkinterSidebar2

import tkinter as tk
from typing import Any, Callable

from .button import Button
from .spacer import Spacer
from .vertical_scrolled_frame import VerticalScrolledFrame


class Sidebar(VerticalScrolledFrame):
    def __init__(self, master: tk.Misc, title: str, show_scrollbar: bool = False):
        super().__init__(master, show_scrollbar)
        self.canvas.config(bg="#232323")
        self.pack_propagate(True)
        self.pack(expand=False, side=tk.LEFT, fill=tk.Y)
        self.selected = None

        Spacer(self.interior, title)

    def add_button(self, text: str, command: Callable[[], Any]):
        btn = Button(
            self.interior, text, lambda btn_self: self.on_click(btn_self, command)
        )

        if self.selected is None:
            btn.click()

    def on_click(self, btn: Button, command: Callable[[], Any]):
        if self.selected != btn:
            if self.selected:
                self.selected.unclick()
            self.selected = btn
            command()
