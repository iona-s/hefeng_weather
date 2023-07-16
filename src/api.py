from typing import Any, Dict, List, Union, Optional

from aiohttp import ClientSession

from .utils import logger
from .models import CityInfo, NowWeather
from .config import HEFENG_KEY, FREE_SUBSCRIBE

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


async def _get(
    url: str,
    *,
    params: Optional[Dict[str, Any]],
) -> Union[str, Dict]:
    async with ClientSession() as session, session.get(
        url,
        params=params,
    ) as resp:
        if resp.status != 200:
            logger.error(f'向{url}查询{params}失败，retcode:{resp.status}')
            return '连接失败'
        resp_content = await resp.json()
        retcode = resp_content['code']
        if retcode != 200:
            return RET_CODE_INFO[retcode]
        return resp_content


async def get_now_weather(location: str) -> Union[str, NowWeather]:
    url = (
        f'https://'
        f'{"dev"if FREE_SUBSCRIBE else ""}'
        f'api.qweather.com/v7/weather/now'
    )
    params = {'key': HEFENG_KEY, 'location': location, 'lang': 'zh'}
    ret = await _get(url, params=params)
    if isinstance(ret, str):
        return ret
    return NowWeather.construct(**ret['now'])


async def get_city_info(
    location: str,
    *,
    adm: str = None,
    search_range: str = 'cn',
    result_number: int = 5,
) -> Union[str, List[CityInfo]]:
    url = 'https://geoapi.qweather.com/v2/city/lookup'
    params = {
        'key': HEFENG_KEY,
        'location': location,
        'adm': adm,
        'range': search_range,
        'number': result_number,
    }
    if adm is None:
        params.pop('adm')
    ret = await _get(url, params=params)
    if isinstance(ret, str):
        return ret
    city_infos = []
    for city in ret['location']:
        city_infos.append(CityInfo.construct(**city))
    return city_infos
