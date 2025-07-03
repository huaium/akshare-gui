import queue
import tkinter as tk
from tkinter import END, scrolledtext
from typing import Literal

from src.config import TEXT_OUTPUT_HEIGHT, TEXT_OUTPUT_WIDTH, WELCOME_MESSAGE
from src.utils import log_utils


class TextOutput(scrolledtext.ScrolledText):
    def __init__(
        self,
        master: tk.Misc,
        width: int = TEXT_OUTPUT_WIDTH,
        height: int = TEXT_OUTPUT_HEIGHT,
        on_message_create: str = WELCOME_MESSAGE,
    ):
        super().__init__(master, width=width, height=height)

        self._queue = queue.Queue()

        self.after(100, self._process_queue)
        self.send_message(on_message_create)

    def send_message(
        self,
        message: str,
        exception: Exception | None = None,
        end: str = "\n",
        color: Literal["red"] | None = None,
    ):
        self._queue.put((message, end, color))

        if color == "red":
            log_utils.error(message)

        if exception:
            log_utils.error(exception)

    def _process_queue(self):
        while not self._queue.empty():
            message, end, color = self._queue.get()
            self._send_message(message, end, color)
        self.after(100, self._process_queue)

    def _send_message(
        self,
        message: str | Exception,
        end="\n",
        color: Literal["red"] | None = None,
    ):
        # make content modifiable
        self.config(state="normal")

        # insert and see are not thread-safe
        self.insert(END, f"{message}{end}")

        # color config
        if color is not None:
            self.tag_add(color, "end-2c linestart", "end-1c lineend")
            self.tag_config(color, foreground=color)

        # scroll to bottom
        self.see(END)

        # avoid user modification
        self.config(state="disabled")
