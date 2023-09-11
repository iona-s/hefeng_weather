from typing import Tuple, Union, Optional

from nonebot import NoneBot
from aiocqhttp import Event as CQEvent
from hoshino import Service, priv, get_bot  # type: ignore

from .src.models import CityInfo
from .src.bot_send import bot_send
from .src.api import get_city_info, get_now_weather, get_hourly_weather
from .src.city_watch_list import (
    add_watch_list,
    get_watch_list,
    get_watched_city,
    remove_watch_list,
)
from .src.exceptions import (
    QueryFailedError,
    CityInWatchListError,
    InvalidArgumentError,
    MissingArgumentError,
    CityNotInWatchListError,
)

# 帮助信息
sv_help = (
    '[地理位置]可为[城市]、[经度] [纬度]、[邮政编码]、[和风天气的城市id]\n'
    '天气 [地理位置]：查询天气\n'
    '未来天气 [地理位置]：查询未来24小时天气\n'
    '未来降雨 [地理位置]：查询未来24小时降雨\n'
    '设置默认城市 [地理位置]：设置默认城市，不指定地理位置则使用默认城市\n'
    '添加/删除群关注城市 [地理位置]：添加/删除群关注城市，'
    '关注后会定时推送未来6小时天气预报\n'
    '查看群城市关注：查看群城市关注'
)

sv = Service(
    name='和风天气',  # 功能名
    use_priv=priv.NORMAL,  # 使用权限
    manage_priv=priv.ADMIN,  # 管理权限
    visible=True,  # 可见性
    enable_on_default=False,  # 默认启用
    help_=sv_help,  # 帮助说明
)

_bot: NoneBot = get_bot()


async def get_city(
    raw_message: str,
    user_id: Optional[Union[str, int]],
) -> Tuple[CityInfo, str, str]:
    """获取城市信息

    :param user_id: 用户qid
    :param raw_message: 原始消息

    :return: CityInfo和对应的location
    ，       输入为经纬度时，location为经纬度，输入为城市名时，location为城市名
            name为城市名
    :rtype: Tuple[CityInfo, str]
    """
    args = raw_message.strip().split()
    arg_count = len(args)
    if arg_count == 0:
        if user_id is None:
            raise InvalidArgumentError
        city_id = get_watched_city(user_id, group=False)
        if city_id is None:
            raise MissingArgumentError
        ret = await get_city_info(city_id, result_number=1)
        city = ret[0]
        location = city.city_id
        name = city.name
    elif arg_count == 1:
        ret = await get_city_info(args[0], result_number=1)
        city = ret[0]
        location = city.city_id
        name = city.name
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
        name = f'{city.name} ({location})'
    else:
        raise InvalidArgumentError
    return city, location, name


@sv.on_prefix(['天气', 'weather'])
async def query_weather(bot: NoneBot, ev: CQEvent):  # noqa: D103
    msg = '发生意外错误'
    raw_message = ev.message.extract_plain_text()
    try:
        city, location, name = await get_city(raw_message, ev.user_id)
        ret = await get_now_weather(location)
        msg = (
            f'{name}的天气：\n'
            f'{ret.weather_description}\n'
            f'气温{ret.temperature}℃\n'
            f'体感温度{ret.feels_temperature}℃\n'
            f'湿度{ret.humidity}%\n'
            f'云量{ret.cloud_amount}%'
        )
    except InvalidArgumentError:
        msg = (
            '错误的命令格式\n应为“天气 [地理位置]”\n[地理位置]可为[城市]、'
            '[经度] [纬度]、[邮政编码]、[和风天气的城市id]'
        )
    except MissingArgumentError:
        msg = '请指定城市或经纬度或设置默认城市'
    except QueryFailedError as e:
        msg = f'查询失败，{e}'
    finally:
        await bot_send(bot, msg, ev=ev)


@sv.on_prefix(['未来天气', '小时天气'])
async def future_weather(bot: NoneBot, ev: CQEvent):  # noqa: D103
    msg = '发生意外错误'
    raw_message = ev.message.extract_plain_text()
    try:
        city, location, name = await get_city(raw_message, ev.user_id)
        ret = await get_hourly_weather(location)
        msg_list = [f'{name}的未来24h天气：']
        for hourly_data in ret:
            msg = (
                f'-> {hourly_data.time.strftime("%H:%M")} '
                f'{hourly_data.weather_description} '
                f'{hourly_data.temperature}℃ '
                f'湿度{hourly_data.humidity}% '
                f'云量{hourly_data.cloud_amount}% '
                f'降水概率{hourly_data.precipitation_probability}%'
            )
            msg_list.append(msg)
        msg = '\n'.join(msg_list)
    except InvalidArgumentError:
        msg = (
            '错误的命令格式\n应为“小时天气 [地理位置]”\n[地理位置]可为[城市]、'
            '[经度] [纬度]、[邮政编码]、[和风天气的城市id]'
        )
    except MissingArgumentError:
        msg = '请指定城市或经纬度或设置默认城市'
    except QueryFailedError as e:
        msg = f'查询失败，{e}'
    finally:
        await bot_send(bot, msg, ev=ev)


@sv.on_prefix(['未来降雨', '小时降雨'])
async def future_precipitation(bot: NoneBot, ev: CQEvent):  # noqa: D103
    msg = '发生意外错误'
    raw_message = ev.message.extract_plain_text()
    try:
        city, location, name = await get_city(raw_message, ev.user_id)
        ret = await get_hourly_weather(location)
        msg_list = [f'{name}的未来24h降雨：']
        for hourly_data in ret:
            msg = (
                f'-> {hourly_data.time.strftime("%H:%M")} '
                f'{hourly_data.weather_description} '
                f'降水概率{hourly_data.precipitation_probability}%'
            )
            msg_list.append(msg)
        msg = '\n'.join(msg_list)
    except InvalidArgumentError:
        msg = (
            '错误的命令格式\n应为“小时降雨 [地理位置]”\n[地理位置]可为[城市]、'
            '[经度] [纬度]、[邮政编码]、[和风天气的城市id]'
        )
    except MissingArgumentError:
        msg = '请指定城市或经纬度或设置默认城市'
    except QueryFailedError as e:
        msg = f'查询失败，{e}'
    finally:
        await bot_send(bot, msg, ev=ev)


@sv.on_prefix(['设置默认城市'])
async def set_default_city(bot: NoneBot, ev: CQEvent):  # noqa: D103
    msg = '发生意外错误'
    raw_message = ev.message.extract_plain_text()
    try:
        city, location, name = await get_city(raw_message, None)
        add_watch_list(ev.user_id, city.city_id, group=False)
        msg = f'已将{name}设置为默认城市'
    except CityInWatchListError:
        msg = f'{raw_message}已经是默认城市'
    except InvalidArgumentError:
        msg = (
            '错误的命令格式\n应为“设置默认城市'
            ' [地理位置]”\n地理位置]可为[城市]、[经度] [纬度]、[邮政编码]、'
            '[和风天气的城市id]'
        )
    except QueryFailedError as e:
        msg = f'设置失败，{e}'
    finally:
        await bot_send(bot, msg, ev=ev)


@sv.on_prefix(['添加群关注城市', '添加群天气关注'])
async def add_watch_city(bot: NoneBot, ev: CQEvent):  # noqa: D103
    msg = '发生意外错误'
    raw_message = ev.message.extract_plain_text()
    try:
        city, location, name = await get_city(raw_message, None)
        add_watch_list(ev.group_id, city.city_id)
        msg = f'已添加{name}到关注列表'
    except CityInWatchListError:
        msg = f'{raw_message}已经在关注列表中'
    except InvalidArgumentError:
        msg = (
            '错误的命令格式\n应为“添加天气关注'
            ' [地理位置]”\n地理位置]可为[城市]、[经度] [纬度]、[邮政编码]、'
            '[和风天气的城市id]'
        )
    except QueryFailedError as e:
        msg = f'添加失败，{e}'
    finally:
        await bot_send(bot, msg, ev=ev)


@sv.on_prefix(['删除群关注城市', '删除群天气关注'])
async def remove_watch_city(bot: NoneBot, ev: CQEvent):  # noqa: D103
    msg = '发生意外错误'
    raw_message = ev.message.extract_plain_text()
    try:
        city, location, name = await get_city(raw_message, None)
        remove_watch_list(ev.group_id, city.city_id)
        msg = f'已从关注列表删除{name}'
    except CityNotInWatchListError:
        msg = f'{raw_message}不在关注列表中'
    except InvalidArgumentError:
        msg = (
            '错误的命令格式\n应为“删除群天气关注'
            ' [地理位置]”\n地理位置]可为[城市]、[经度] [纬度]、[邮政编码]、'
            '[和风天气的城市id]'
        )
    except QueryFailedError as e:
        msg = f'删除失败，{e}'
    finally:
        await bot_send(bot, msg, ev=ev)


@sv.on_rex(r'^(查看)?群(城市|天气)关注$')
async def show_watch_list(bot: NoneBot, ev: CQEvent):  # noqa: D103
    msg = '发生意外错误'
    try:
        watch_list = get_watched_city(ev.group_id)
        if watch_list is None:
            msg = '关注列表为空'
        else:
            city_list = []
            for city_id in watch_list:
                city = await get_city_info(city_id, result_number=1)
                city_list.append(city[0].name)
            msg = '关注列表：\n' + '，'.join(city_list)
    finally:
        await bot_send(bot, msg, ev=ev)


# 定时任务
@sv.scheduled_job('cron', hour='7, 12, 16')
async def hourly_weather_forcast():
    """每天7点、12点、18点推送天气预报"""
    watch_list = get_watch_list()
    if watch_list is None:
        return
    for group_id, city_list in watch_list.items():
        msg_list = []
        for city_id in city_list:
            city = await get_city_info(city_id, result_number=1)
            detail_msg_list = [f'{city[0].name}的未来6h降雨：']
            ret = await get_hourly_weather(city_id)
            for hourly_data in ret[:6]:
                msg = (
                    f'-> {hourly_data.time.strftime("%H:%M")} '
                    f'{hourly_data.weather_description} '
                    f'{hourly_data.temperature}℃ '
                    f'湿度{hourly_data.humidity}% '
                    f'云量{hourly_data.cloud_amount}% '
                    f'降水概率{hourly_data.precipitation_probability}%'
                )
                detail_msg_list.append(msg)
            msg_list.append('\n'.join(detail_msg_list))
        msg = '\n----------\n'.join(msg_list)
        await bot_send(_bot, msg, target_id=group_id)
