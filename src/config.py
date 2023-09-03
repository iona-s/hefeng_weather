from pathlib import Path

from pydantic import BaseModel
from yaml import safe_dump, safe_load

from .logger import logger

CONFIG_PATH = Path(__file__).resolve().parent.parent / 'config.yml'


class Config(BaseModel):
    """项目配置项"""

    HEFENG_KEY: str = ''
    FREE_SUBSCRIBE: bool = True
    SEND_MESSAGE_INTERVAL: float = 0.5

    @classmethod
    def load(cls) -> 'Config':
        """加载配置项"""
        if not CONFIG_PATH.exists():
            cfg = cls()
            cfg.save()
            logger.warning('配置文件不存在，已创建默认配置文件')
        else:
            with CONFIG_PATH.open(encoding='utf-8') as f:
                cfg = cls(**safe_load(f))
        if not cfg.HEFENG_KEY:
            error_msg = '和风天气key为空，天气功能将无法使用'
            raise ValueError(error_msg)
        return cfg

    def save(self) -> None:
        """保存配置项"""
        with CONFIG_PATH.open('w', encoding='utf-8') as f:
            f.write(
                safe_dump(self.dict(), allow_unicode=True, sort_keys=False),
            )


config = Config.load()
