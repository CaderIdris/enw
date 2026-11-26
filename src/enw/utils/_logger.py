import logging
import os

_level = logging.DEBUG if os.getenv("PYLOGDEBUG") else logging.INFO
_format_str = (
    "%(asctime)s - %(funcName)s - %(levelname)s - %(message)s"
    if os.getenv("PYLOGDEBUG") else "%(asctime)s - %(message)s"
)

_handler = logging.StreamHandler()
_handler.setLevel(_level)

_formatter = logging.Formatter(_format_str)
_handler.setFormatter(_formatter)

logger = logging.getLogger("enw")
logger.setLevel(_level)
logger.addHandler(_handler)
