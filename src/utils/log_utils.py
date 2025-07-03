import logging
import traceback

_logger = logging.getLogger("app")
_logger.setLevel(logging.DEBUG)

_console_handler = logging.StreamHandler()
_console_handler.setLevel(logging.DEBUG)

formatter = logging.Formatter("[%(asctime)s] %(levelname)s - %(name)s - %(message)s")
_console_handler.setFormatter(formatter)

_logger.addHandler(_console_handler)


def debug(message: str):
    _logger.debug(message)


def info(message: str):
    _logger.info(message)


def warning(message: str):
    _logger.warning(message)


def error(message: str | Exception):
    if isinstance(message, Exception):
        return _logger.error(str(message) + traceback.format_exc())

    _logger.error(message)
