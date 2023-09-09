from typing import Optional


class QueryFailedError(Exception):
    """api查询失败"""

    def __init__(self, message: Optional[str] = None):  # noqa: D107
        if message is not None:
            super().__init__(message)


class MissingArgumentError(Exception):
    """用户输入的指令缺少参数"""

    def __init__(self, message: Optional[str] = None):  # noqa: D107
        if message is not None:
            super().__init__(message)


class InvalidArgumentError(Exception):
    """用户输入的指令有误"""

    def __init__(self, message: Optional[str] = None):  # noqa: D107
        if message is not None:
            super().__init__(message)


class CityInWatchListError(Exception):
    """城市已经在关注列表中"""

    def __init__(self, message: Optional[str] = None):  # noqa: D107
        if message is not None:
            super().__init__(message)


class CityNotInWatchListError(Exception):
    """城市不在关注列表中"""

    def __init__(self, message: Optional[str] = None):  # noqa: D107
        if message is not None:
            super().__init__(message)
