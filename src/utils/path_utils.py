import sys
from pathlib import Path


def res_path(relative_path: str | Path) -> Path:
    if hasattr(sys, "_MEIPASS"):
        return Path(getattr(sys, "_MEIPASS")) / "res" / relative_path
    return cwd() / "res" / relative_path


def res_path_posix(relative_path: str | Path) -> str:
    return res_path(relative_path).as_posix()


def cwd() -> Path:
    if hasattr(sys, "frozen"):
        path = Path(sys.executable).parent
        if sys.platform == "darwin":
            return path.parent.parent.parent
        else:
            # Windows/Linux
            return path.parent
    return Path.cwd().resolve()
