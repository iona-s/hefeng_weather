from hashlib import md5
from typing import Optional
from json import JSONEncoder
from datetime import date, datetime


def generate_cache_name(func_name: str, kwargs: dict) -> str:
    """将参数字典转换为字符串"""
    name = f'{func_name}_' + ','.join(f'{k}={v}' for k, v in kwargs.items())
    return md5(name.encode()).hexdigest()


# subclass JSONEncoder
class DateTimeEncoder(JSONEncoder):
    """Override the default method to serialize datetime"""

    def default(self, obj) -> Optional[str]:  # noqa: D102
        if isinstance(obj, (date, datetime)):
            return obj.isoformat()
        return None
