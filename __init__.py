from nonebot import NoneBot
from aiocqhttp import Event as CQEvent
from hoshino import Service, priv, get_bot  # type: ignore

from .src.bot_send import bot_send
from .src.api import get_city_info, get_now_weather

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


@sv.on_prefix(['天气', 'weather'])
def query_weather(bot: NoneBot, ev: CQEvent):
    raw_message = ev.raw_message.strip()
    arg_count = len(raw_message)
    if arg_count == 1:
        ret = await get_city_info(raw_message[0], result_number=1)
        if isinstance(ret, str):
            await bot_send(bot, f'查询失败，{ret}', ev=ev)
            return
        city = ret[0]
        location = city.city_id
    elif arg_count == 2:
        location = ','.join(raw_message)
    else:
        msg = '错误的命令格式\n应为“天气” + [城市]或“天气” + [经度] + [纬度]'
        await bot_send(bot, msg, ev=ev)
        return

    ret = await get_now_weather(location)
    if isinstance(ret, str):
        await bot_send(bot, f'查询失败，{ret}', ev=ev)
        return
