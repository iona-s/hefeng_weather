from pathlib import Path

from pydantic import BaseModel
from yaml import safe_dump, safe_load

from .logger import logger

CONFIG_PATH = Path(__file__).resolve().parent.parent / 'config.yml'


class Config(BaseModel):
    HEFENG_KEY: str = ''
    FREE_SUBSCRIBE: bool = True
    SEND_MESSAGE_INTERVAL: float = 0.5

    @classmethod
    def load(cls) -> 'Config':
        if not CONFIG_PATH.exists():
            cfg = cls()
            cfg.save()
            logger.warning('配置文件不存在，已创建默认配置文件')
        else:
            with CONFIG_PATH.open(encoding='utf-8') as f:
                cfg = cls(**safe_load(f))
        if not cfg.HEFENG_KEY:
            raise ValueError('和风天气key为空，天气功能将无法使用')
        return cfg

    def save(self) -> None:
        with CONFIG_PATH.open('w', encoding='utf-8') as f:
            f.write(
                safe_dump(self.dict(), allow_unicode=True, sort_keys=False),
            )


config = Config.load()
