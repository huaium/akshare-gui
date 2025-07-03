import tkinter as tk
import tkinter.ttk as ttk
from dataclasses import dataclass
from pathlib import Path
from tkinter import messagebox
from typing import Any, Callable

from src.enums import ApiItem, SideItem
from src.utils import grid_utils

from .browse_frame import BrowseFrame
from .labeled_entry import LabeledEntry
from .option_frame import OptionFrame
from .process_buttons import ProcessButtons
from .text_output import TextOutput


class ControlFrame(ttk.Frame):
    @dataclass
    class ControlData:
        input_fpath_str: str
        output_fpath_str: str
        api_item: ApiItem
        indicator_item: str

    def __init__(
        self,
        master: tk.Misc,
        side_item: SideItem,
        on_start: Callable[[ControlData], Any],
    ):
        super().__init__(master)

        # text output widget (before add to grid)
        self._text_output = TextOutput(master=self)
        self._browse_frame = BrowseFrame(master=self)
        self._warning_label = ttk.Label(
            self,
            text="(如不选择输出文件夹，则默认为同文件夹下的 AKShare_Output 目录)",
        )
        self._output_fname_entry = LabeledEntry(
            master=self,
            label_text="请输入要导出的文件名:",
            entry_text=f"{side_item.value}Output.xlsx",
        )
        self._option_frame = OptionFrame(
            master=self,
            api_items=side_item.api_items,
            indicator_items=side_item.indicator_items,
        )
        self._process_frame = ProcessButtons(
            master=self,
            template_path=side_item.template_fpath,
            on_start=self._check_and_start,
        )

        self._on_start = on_start
        self._create_widgets()

    @property
    def text_output(self):
        return self._text_output

    def _create_widgets(self):
        # browse frame
        grid_utils.add(master=self, widget=self._browse_frame, column=0)

        # warning label
        grid_utils.add(master=self, widget=self._warning_label, column=0)

        # output fname entry
        grid_utils.add(master=self, widget=self._output_fname_entry, column=0)

        # option frame
        grid_utils.add(master=self, widget=self._option_frame, column=0)

        # process buttons frame
        grid_utils.add(master=self, widget=self._process_frame, column=0)

        # add text output to grid
        grid_utils.add(master=self, widget=self._text_output, column=0, pady=0)

    def _check_and_start(self):
        # check input fpath
        input_fpath_str = self._browse_frame.input_fpath_str
        if not input_fpath_str:
            messagebox.showerror("错误", "请选择一个输入文件")
            return

        if not Path(input_fpath_str).exists():
            messagebox.showerror("错误", "文件不存在或路径错误")
            return

        # check output fpath
        output_path_str = self._browse_frame.output_path_str
        if not output_path_str:
            messagebox.showerror("错误", "请选择一个输出文件夹")
            return

        output_path = Path(output_path_str)
        if not output_path.exists():
            output_path.mkdir(parents=True)

        output_fpath = output_path / self._output_fname_entry.text

        return self._on_start(
            self.ControlData(
                input_fpath_str=input_fpath_str,
                output_fpath_str=output_fpath.as_posix(),
                api_item=self._option_frame.api_item,
                indicator_item=self._option_frame.indicator_item,
            )
        )
