# Original author: Olikonsti
# Modified from: https://github.com/Olikonsti/TkinterSidebar2

import platform
import tkinter as tk
import tkinter.ttk as ttk
from functools import partial


class VerticalScrolledFrame(ttk.Frame):
    """
    A pure Tkinter scrollable frame that actually works!
    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    * This comes from a different naming of the the scrollwheel 'button', on different systems.
    """

    def __init__(
        self,
        master: tk.Misc,
        show_scrollbar: bool,
        *args,
        **kw,
    ):
        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event: tk.Event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion=(0, 0, *size))

            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        def _configure_canvas(event: tk.Event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())

        super().__init__(master, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        if show_scrollbar:
            vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(
            self, bd=0, highlightthickness=0, yscrollcommand=vscrollbar.set
        )
        self.canvas = canvas
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = ttk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior, anchor=tk.NW)

        _bind_to_mousewheel, _unbind_from_mousewheel = self._mousewheel_binding(canvas)

        interior.bind("<Configure>", _configure_interior)
        canvas.bind("<Configure>", _configure_canvas)
        canvas.bind("<Enter>", _bind_to_mousewheel)
        canvas.bind("<Leave>", _unbind_from_mousewheel)

    def _mousewheel_binding(self, canvas: tk.Canvas):
        return (
            self._mousewheel_binding_linux(canvas)
            if platform.system() == "Linux"
            else self._mousewheel_binding_other(canvas)
        )

    def _mousewheel_binding_linux(self, canvas: tk.Canvas):
        def _on_mousewheel(event: tk.Event, scroll):
            canvas.yview_scroll(int(scroll), "units")

        def _bind_to_mousewheel(event: tk.Event):
            canvas.bind_all("<Button-4>", partial(_on_mousewheel, scroll=-1))
            canvas.bind_all("<Button-5>", partial(_on_mousewheel, scroll=1))

        def _unbind_from_mousewheel(event: tk.Event):
            canvas.unbind_all("<Button-4>")
            canvas.unbind_all("<Button-5>")

        return _bind_to_mousewheel, _unbind_from_mousewheel

    def _mousewheel_binding_other(self, canvas: tk.Canvas):
        def _on_mousewheel(event: tk.Event):
            canvas.yview_scroll(int(-1 * (event.delta / 120)), "units")

        def _bind_to_mousewheel(event: tk.Event):
            canvas.bind_all("<MouseWheel>", _on_mousewheel)

        def _unbind_from_mousewheel(event: tk.Event):
            canvas.unbind_all("<MouseWheel>")

        return _bind_to_mousewheel, _unbind_from_mousewheel
