import shutil
import tkinter as tk
import tkinter.ttk as ttk
from pathlib import Path
from tkinter import E, W, filedialog, messagebox
from typing import Any, Callable

from src.utils import grid_utils, log_utils, path_utils, thread_utils


class ProcessButtons(ttk.Frame):
    def __init__(
        self,
        master: tk.Misc,
        template_path: Path,
        on_start: Callable[[], Any],
    ):
        super().__init__(master)

        # set column weight to ensure centering
        self.columnconfigure(0, weight=1)
        self.columnconfigure(1, weight=1)

        # buttons
        self._button_start = ttk.Button(
            self,
            text="Start!",
            command=lambda: self._start(on_start=on_start),
        )
        self._button_export = ttk.Button(
            self,
            text="Input Sheet 模板",
            command=lambda: self._export_demo(template_path),
        )
        self._create_widgets()

    def _create_widgets(self):
        grid_utils.add(
            master=self, widget=self._button_start, column=0, pady=0, sticky=E
        )
        grid_utils.add(
            master=self, widget=self._button_export, column=1, pady=0, sticky=W
        )

    def _export_demo(self, input_template_path: Path):
        save_path = filedialog.asksaveasfilename(
            title="另存为",
            defaultextension=".xlsx",
            filetypes=[("Excel files", "*.xlsx"), ("All Files", "*.*")],
            initialdir=path_utils.desktop(),
            initialfile=input_template_path.name,
        )

        if save_path:
            try:
                shutil.copyfile(input_template_path, save_path)
                messagebox.showinfo("成功", f"文件已保存到 {save_path}")
            except Exception as e:
                messagebox.showerror("错误", "另存为失败")
                log_utils.error(e)

    def _start(
        self,
        on_start: Callable[[], Any],
    ):
        # main thread cannot be blocked in Tk, so a callback is needed
        thread_utils.thread_it(func=on_start, join=False)
