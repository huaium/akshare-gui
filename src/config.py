from typing import Any, Type, TypeVar

import tomllib

from .utils import path_utils

_config_path = path_utils.res_path("config.toml")

if not _config_path.exists():
    raise FileNotFoundError("Config file not found.")
with open(_config_path, "rb") as f:
    _cfg = tomllib.load(f)

T = TypeVar("T")


def _get_typed(d: dict, key: str, expected_type: Type[T]) -> T:
    value = d.get(key)
    if value is None:
        raise KeyError(f"Key '{key}' not found")
    if not isinstance(value, expected_type):
        raise TypeError(
            f"Value for '{key}' is not of type {expected_type.__name__}: got {type(value).__name__}"
        )
    return value


def _get_cfg_typed(key: str, expected_type: Type[T]) -> T:
    return _get_typed(_cfg, key, expected_type)


def _get_str(key: str) -> str:
    return _get_cfg_typed(key, str)


def _get_int(key: str) -> int:
    return _get_cfg_typed(key, int)


def _get_dict(key: str) -> dict[str, Any]:
    return _get_cfg_typed(key, dict)


TEXT_OUTPUT_WIDTH: int = _get_int("text_output_width")
TEXT_OUTPUT_HEIGHT: int = _get_int("text_output_height")
ENTRY_WIDTH: int = _get_int("entry_width")
DEFAULT_PADY: int = _get_int("default_pady")
APP_NAME: str = _get_str("app_name")
WELCOME_MESSAGE: str = _get_str("welcome_message")
