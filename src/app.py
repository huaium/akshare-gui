import tkinter as tk
import tkinter.ttk as ttk
from tkinter import BOTH, LEFT

from .client import Client
from .config import (
    APP_NAME,
    DEFAULT_PADY,
)
from .enums import SideItem
from .sidebar import Sidebar
from .utils import thread_utils
from .widgets import ControlFrame


class App:
    def __init__(self):
        self.is_closing = False

        # root config
        self.root = tk.Tk()
        self.root.title(APP_NAME)
        self.root.bind("<Destroy>", self._on_close)

        # basic framework inside the window
        self.left_frame, self.right_frame = self._create_parent_frames()

        # every SideItem is accompanied by a SideItemRes
        self.side_item_map: dict[SideItem, ControlFrame] = {}

        self._create_sidebar_widget(self.left_frame)

    def _show_frame(self, side_item: SideItem):
        """
        Called immediately after the first button of sidebar was added.
        """
        if side_item not in self.side_item_map:
            client = Client(side_item=side_item)
            control_frame = ControlFrame(
                master=self.right_frame,
                side_item=side_item,
                on_start=lambda control_data: client.run(
                    input_fpath_str=control_data.input_fpath_str,
                    output_fpath_str=control_data.output_fpath_str,
                    api_item=control_data.api_item,
                    indicator_item=control_data.indicator_item,
                ),
            )  # lambda is lazy
            client.text_output = control_frame.text_output
            self.side_item_map[side_item] = control_frame

            control_frame.grid(row=0, column=0, pady=DEFAULT_PADY)

        self.side_item_map[side_item].lift()

    def _create_parent_frames(self):
        left_frame = ttk.Frame(self.root)
        left_frame.pack(side=LEFT, fill=BOTH, expand=True)

        right_frame = ttk.Frame(self.root)
        right_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

        return left_frame, right_frame

    def _create_sidebar_widget(self, master: ttk.Frame):
        sidebar = Sidebar(master, APP_NAME)

        # the first button added will trigger its command
        for item in SideItem:
            sidebar.add_button(item.value, command=lambda i=item: self._show_frame(i))

    def _on_close(self, event: tk.Event | None = None):
        if not self.is_closing:
            self.is_closing = True

            thread_utils.shutdown()

            self.is_closing = False

    def run(self):
        self.root.update_idletasks()
        self.root.lift()
        self.root.focus_force()
        self.root.mainloop()
