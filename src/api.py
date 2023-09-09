from typing import Any, Dict, List, Union, Optional

from aiohttp import ClientSession
from pydantic import parse_obj_as

from .config import config
from .logger import logger
from .api_cache import use_cache
from .exceptions import QueryFailedError
from .models import CityInfo, CityWeatherApi

RET_CODE_INFO = {
    '204': '请求成功，但你查询的地区暂时没有你需要的数据。',
    '400': '请求参数错误，请联系管理员。',
    '401': '认证失败。',
    '402': '超过访问次数或余额不足以支持继续访问服务，请联系管理员。',
    '403': '无访问权限，请联系管理员。',
    '404': '查询的数据或地区不存在。',
    '429': '超过限定的每分钟访问次数',
    '500': '无响应或超时.',
}

BASE_PARAMS = {
    'key': config.HEFENG_KEY,
}


async def _get(
    url: str,
    *,
    params: Optional[Dict[str, Any]] = None,
) -> Dict:
    params = {**BASE_PARAMS, **(params or {})}
    async with ClientSession() as session, session.get(
        url,
        params=params,
    ) as resp:
        logger.debug(f'使用{url}查询{params}')
        if resp.status != 200:
            logger.error(f'查询失败 status code{resp.status}')
            msg = '连接失败'
            raise QueryFailedError(msg)
        resp_content = await resp.json()
        logger.debug(f'返回值 {resp_content}')
        retcode = resp_content['code']
        if retcode != '200':
            retcode_info = RET_CODE_INFO[retcode]
            logger.error(f'查询失败 retcode{retcode}{retcode_info}')
            raise QueryFailedError(retcode_info)
        return resp_content


@use_cache(List[CityInfo], config.CITY_INFO_TTL)
async def get_city_info(
    location: str,
    *,
    adm: str = None,
    search_range: str = 'cn',
    result_number: int = 5,
) -> List[CityInfo]:
    """使用城市id或经纬度查询城市信息"""
    url = 'https://geoapi.qweather.com/v2/city/lookup'
    params = {
        'location': location,
        'adm': adm,
        'range': search_range,
        'number': result_number,
    }
    if adm is None:
        params.pop('adm')
    resp = await _get(url, params=params)
    return parse_obj_as(List[CityInfo], resp['location'])


@use_cache(CityWeatherApi.NowWeather, config.WEATHER_INFO_TTL)
async def get_now_weather(
    location: str,
) -> CityWeatherApi.NowWeather:
    """使用城市id或经纬度查询城市天气"""
    url = (
        'https://'
        f'{"dev"if config.FREE_SUBSCRIBE else ""}'
        'api.qweather.com/v7/weather/now'
    )
    params = {'location': location, 'lang': 'zh'}
    ret = await _get(url, params=params)
    return CityWeatherApi.NowWeather.parse_obj(ret['now'])


@use_cache(List[CityWeatherApi.HourlyWeather], config.WEATHER_INFO_TTL)
async def get_hourly_weather(
    location: str,
) -> Union[str, List[CityWeatherApi.HourlyWeather]]:
    """使用城市id或经纬度查询小时天气"""
    url = (
        'https://'
        f'{"dev"if config.FREE_SUBSCRIBE else ""}'
        'api.qweather.com/v7/weather/24h'
    )
    params = {'location': location, 'lang': 'zh'}
    ret = await _get(url, params=params)
    return [
        CityWeatherApi.HourlyWeather.parse_obj(data) for data in ret['hourly']
    ]
