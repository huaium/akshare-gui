import os
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import filedialog, messagebox

from src.config import DEFAULT_PADY, ENTRY_WIDTH
from src.utils import grid_utils, log_utils, path_utils

from .labeled_entry import LabeledEntry


class BrowseFrame(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        entry_width: int = ENTRY_WIDTH,
        pady: int = DEFAULT_PADY,
    ):
        super().__init__(master)

        self._input_fpath_entry: LabeledEntry = LabeledEntry(
            master=self,
            label_text="请选择要导入的 Input Sheet:",
            entry_width=entry_width,
            pady=pady,
        )
        self._output_path_entry: LabeledEntry = LabeledEntry(
            master=self,
            label_text="请选择要导出的目标文件夹:",
            entry_width=entry_width,
            pady=pady,
        )
        self._create_widgets(pady)

    # no setter for those two, to avoid user modification
    @property
    def input_fpath_str(self) -> str:
        return self._input_fpath_entry.text

    @property
    def output_path_str(self) -> str:
        return self._output_path_entry.text

    def _on_file_select(self, file_path: Path):
        self._input_fpath_entry.text = file_path.as_posix()
        new_dir = Path(file_path).parent / "AKShare_Output"
        self._output_path_entry.text = new_dir.as_posix()

    def _reset_input_fpath(self):
        self._input_fpath_entry.text = ""

    def _reset_output_path(self):
        self._output_path_entry.text = ""

    def _browse_file(self):
        try:
            file_path_str = filedialog.askopenfilename(
                title="选择 Excel 文件",
                filetypes=[("Excel files", "*.xlsx"), ("Excel files", "*.xls")],
                initialdir=path_utils.desktop(),
            )

            if file_path_str:
                file_path = Path(file_path_str)
                if not file_path.exists():
                    messagebox.showerror("错误", "所选文件不存在")
                    return

                if not os.access(file_path_str, os.R_OK):
                    messagebox.showerror("错误", "无法读取所选文件，请检查文件权限")
                    return

                self._on_file_select(file_path)

        except Exception as e:
            messagebox.showerror("错误", "选择文件时发生错误")
            log_utils.error(e)
            self._reset_input_fpath()

    def _browse_dest(self):
        try:
            folder_path_str = filedialog.askdirectory(
                title="选择导出目标文件夹",
                initialdir=Path(self.input_fpath_str).parent
                if self.input_fpath_str
                else path_utils.desktop(),
            )

            if folder_path_str:
                folder_path = Path(folder_path_str)
                # check if exists
                if not folder_path.exists():
                    if messagebox.askyesno("确认", "所选文件夹不存在，是否创建？"):
                        try:
                            folder_path.mkdir()
                        except Exception as e:
                            messagebox.showerror("错误", "创建文件夹失败")
                            log_utils.error(e)
                            return
                    else:
                        return

                # check access permission
                if not os.access(folder_path_str, os.W_OK):
                    messagebox.showwarning(
                        "警告",
                        "所选文件夹可能没有写入权限，请选择其他文件夹",
                    )
                    return

                self._output_path_entry.text = folder_path.as_posix()

        except Exception as e:
            messagebox.showerror("错误", "选择文件夹时发生错误")
            log_utils.error(e)
            self._reset_output_path()

    def _create_widgets(self, pady: int = DEFAULT_PADY):
        # input path
        grid_utils.add(master=self, widget=self._input_fpath_entry, column=0, pady=0)
        button_browse_input: ttk.Button = ttk.Button(
            self, text="浏览", command=self._browse_file
        )
        grid_utils.add(master=self, widget=button_browse_input, column=0, pady=pady)

        # output path
        grid_utils.add(master=self, widget=self._output_path_entry, column=1, pady=0)
        button_browse_output: ttk.Button = ttk.Button(
            self, text="浏览", command=self._browse_dest
        )
        grid_utils.add(master=self, widget=button_browse_output, column=1, pady=pady)
