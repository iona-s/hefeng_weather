from typing import Optional


class QueryFailedError(Exception):
    def __init__(self, message: Optional[str] = None):
        if message is not None:
            super().__init__(message)


class InvalidArgumentError(Exception):
    def __init__(self, message: Optional[str] = None):
        if message is not None:
            super().__init__(message)
