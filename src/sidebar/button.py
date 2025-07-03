# Original author: Olikonsti
# Modified from: https://github.com/Olikonsti/TkinterSidebar2

import tkinter as tk
from typing import Any, Callable


class Button(tk.Canvas):
    def __init__(
        self,
        master: tk.Misc,
        text: str,
        command: Callable[["Button"], Any],
        *args,
        **kwargs,
    ):
        self.frame_color = "#232323"
        self.hover_color = "#4D4c4c"

        super().__init__(
            master,
            width=200,
            height=35,
            bg=self.frame_color,
            highlightbackground=self.frame_color,
            *args,
            **kwargs,
        )
        self.pack()

        self.selected = False
        self.command = command

        self.text = tk.Label(self, text=text, bg=self.frame_color, fg="lightgrey")
        self.text.place(x=20, y=10)

        self.bind_events()

    def bind_events(self):
        for widget in (self, self.text):
            widget.bind("<Enter>", self._hover)
            widget.bind("<Leave>", self._unhover)
            widget.bind("<Button-1>", self.click)

    def _hover(self, event: tk.Event | None = None):
        if not self.selected:
            self.config(highlightbackground=self.hover_color, bg=self.hover_color)
            self.text.config(bg=self.hover_color)

    def _unhover(self, event: tk.Event | None = None):
        if not self.selected:
            self.config(highlightbackground=self.frame_color, bg=self.frame_color)
            self.text.config(bg=self.frame_color)

    def click(self, event: tk.Event | None = None):
        if not self.selected:
            self.selected = True
            self.config(highlightbackground=self.hover_color, bg=self.hover_color)
            self.text.config(bg=self.hover_color)

            self.command(self)

    def unclick(self, event: tk.Event | None = None):
        if self.selected:
            self.selected = False
            self.config(highlightbackground=self.frame_color, bg=self.frame_color)
            self.text.config(bg=self.frame_color)
