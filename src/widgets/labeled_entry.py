import tkinter as tk
import tkinter.ttk as ttk

from src.config import DEFAULT_PADY, ENTRY_WIDTH
from src.utils import grid_utils


class LabeledEntry(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        label_text: str,
        entry_text: str = "",
        entry_width: int = ENTRY_WIDTH,
        pady: int = DEFAULT_PADY,
    ):
        super().__init__(master)

        self._variable: tk.StringVar = tk.StringVar(value=entry_text)
        self._label: ttk.Label = ttk.Label(self, text=label_text)
        self._entry: ttk.Entry = ttk.Entry(
            self, width=entry_width, textvariable=self._variable
        )
        self._create_widgets(pady=pady)

    @property
    def text(self) -> str:
        return self._variable.get()

    @text.setter
    def text(self, value: str):
        self._variable.set(value)

    def _create_widgets(self, pady: int = DEFAULT_PADY):
        grid_utils.add(master=self, widget=self._label, column=0, pady=pady)
        grid_utils.add(master=self, widget=self._entry, column=0, pady=pady)
