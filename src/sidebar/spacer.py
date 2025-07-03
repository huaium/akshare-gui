# Original author: Olikonsti
# Modified from: https://github.com/Olikonsti/TkinterSidebar2

import tkinter as tk


class Spacer(tk.Canvas):
    def __init__(self, master: tk.Misc, text: str, *args, **kwargs):
        self.frame_color = "#232323"

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

        self.text = tk.Label(self, text=text, bg=self.frame_color, fg="lightgrey")
        self.text.place(x=10, y=10)
