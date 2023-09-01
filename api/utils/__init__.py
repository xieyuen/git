from ...utils import hash, batch_hash, disable_in_py3
from ...utils.register import Register, functions, classes
from ...utils.logger import logger, Logger


__all__ = [
    # --- 更方便的 hash 函数 --- #
    "hash", "batch_hash",

    # --- 注册器 --- #
    "Register", "functions", "classes",

    # --- 较方便的 logger --- #
    "logger", "Logger",

    # --- Python 3 中删除的功能 --- #
    "disable_in_py3",
]
