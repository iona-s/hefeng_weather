from typing import Tuple

from nonebot import NoneBot
from aiocqhttp import Event as CQEvent
from hoshino import Service, priv, get_bot  # type: ignore

from .src.models import CityInfo
from .src.bot_send import bot_send
from .src.api import get_city_info, get_now_weather
from .src.exceptions import QueryFailedError, InvalidArgumentError

sv_help = '''
这是帮助
'''.strip()

sv = Service(
    name='和风天气',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=False,  # 默认启用
    help_=sv_help,  # 帮助说明
)

_bot: NoneBot = get_bot()


async def get_city(raw_message: str) -> Tuple[CityInfo, str]:
    """

    :param raw_message: 原始消息
    :return: CityInfo和对应的locatio
    ，       输入为经纬度时，location为经纬度，输入为城市名时，location为城市名
    :rtype: Tuple[CityInfo, str]
    """
    args = raw_message.strip().split()
    arg_count = len(args)
    if arg_count == 1:
        ret = await get_city_info(args[0], result_number=1)
        city = ret[0]
        location = city.city_id
    elif arg_count == 2:
        try:
            longitude, latitude = map(float, args)
        except ValueError:
            raise InvalidArgumentError from None
        if not (-180 <= longitude <= 180 and -90 <= latitude <= 90):
            raise InvalidArgumentError
        location = f'{longitude},{latitude}'
        ret = await get_city_info(location, result_number=1)
        city = ret[0]
    else:
        raise InvalidArgumentError
    return city, location


@sv.on_prefix(['天气', 'weather'])
async def query_weather(bot: NoneBot, ev: CQEvent):
    try:
        raw_message = ev.message.extract_plain_text()
        city, location = await get_city(raw_message)
        ret = await get_now_weather(location)
        msg = (
            f'{city.name}的天气：\n'
            f'{ret.weather_description}\n'
            f'气温{ret.temperature}℃\n'
            f'体感温度{ret.feels_temperature}℃\n'
            f'湿度{ret.humidity}%\n'
            f'云量{ret.cloud_amount}%'
        )
        await bot_send(bot, msg, ev=ev)
    except QueryFailedError as e:
        await bot_send(bot, f'查询失败，{e}', ev=ev)
    except InvalidArgumentError:
        msg = '错误的命令格式\n应为“天气” + [城市]或“天气” + [经度] + [纬度]'
        await bot_send(bot, msg, ev=ev)


@sv.on_prefix(['未来降雨'])
async def future_precipitation(bot: NoneBot, ev: CQEvent):
    pass
