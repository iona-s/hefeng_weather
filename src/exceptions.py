from typing import Optional


class QueryFailedError(Exception):
    """api查询失败"""

    def __init__(self, message: Optional[str] = None):  # noqa: D107
        if message is not None:
            super().__init__(message)


class InvalidArgumentError(Exception):
    """用户输入的指令有误"""

    def __init__(self, message: Optional[str] = None):  # noqa: D107
        if message is not None:
            super().__init__(message)
