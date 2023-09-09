from hashlib import md5


def generate_cache_name(func_name: str, args: dict) -> str:
    """将参数字典转换为字符串"""
    name = func_name + ','.join(f'{k}={v}' for k, v in args.items())
    return md5(name.encode()).hexdigest()
