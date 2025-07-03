import tkinter as tk
import tkinter.ttk as ttk
from tkinter import EW, E, W
from typing import Sequence

from src.config import DEFAULT_PADY
from src.enums import ApiItem
from src.utils import grid_utils


class OptionFrame(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        api_items: Sequence[str],
        indicator_items: Sequence[str],
        pady: int = DEFAULT_PADY,
    ):
        super().__init__(master)

        self._api_item: tk.StringVar = tk.StringVar(value=api_items[0])
        self._api_items: Sequence[str] = api_items

        self._indicator_item: tk.StringVar = tk.StringVar(value=indicator_items[0])
        self._indicator_items: Sequence[str] = indicator_items

        self._create_widgets(pady)

    @property
    def api_item(self) -> ApiItem:
        return ApiItem(self._api_item.get())

    @property
    def indicator_item(self) -> str:
        return self._indicator_item.get()

    def _create_widgets(self, pady: int = DEFAULT_PADY):
        # set column weight to ensure centering
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        api_label = ttk.Label(self, text="API 接口(若多次失败请修改): ")
        grid_utils.add(master=self, widget=api_label, column=0, sticky=E, pady=pady)
        option_api = ttk.OptionMenu(
            self,
            self._api_item,
            self._api_items[0] if self._api_items else "",
            *self._api_items,
        )
        grid_utils.add(master=self, widget=option_api, column=1, sticky=W, pady=pady)

        spacer = ttk.Label(self, text="", width=2)
        grid_utils.add(master=self, widget=spacer, column=3, sticky=EW, pady=pady)

        indicator_label = ttk.Label(self, text="数据类别: ")
        grid_utils.add(
            master=self, widget=indicator_label, column=4, sticky=E, pady=pady
        )
        option_indicator = ttk.OptionMenu(
            self,
            self._indicator_item,
            self._indicator_items[0] if self._indicator_items else "",
            *self._indicator_items,
        )
        grid_utils.add(
            master=self, widget=option_indicator, column=5, sticky=W, pady=pady
        )
