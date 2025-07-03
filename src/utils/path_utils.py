import sys
from pathlib import Path


def res_path(relative_path: str | Path) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(getattr(sys, "_MEIPASS")) / "res" / relative_path
    return Path.cwd() / "res" / relative_path


def res_path_posix(relative_path: str | Path) -> str:
    return res_path(relative_path).as_posix()


def desktop() -> Path:
    return (Path.home() / "Desktop").resolve()
