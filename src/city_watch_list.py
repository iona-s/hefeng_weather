from json import dump, load
from typing import Dict, List, Union, Optional

from .define import WATCH_LIST_DIR
from .exceptions import CityInWatchListError, CityNotInWatchListError

GROUP_WATCH_LIST_PATH = WATCH_LIST_DIR / 'group_watch_list.json'
SELF_WATCH_LIST_PATH = WATCH_LIST_DIR / 'self_watch_list.json'
GROUP_WATCH_LIST = Dict[int, List[str]]  # 群号，城市id列表
SELF_WATCH_LIST = Dict[int, str]  # qid，城市id


def get_watch_list(
    group: bool = True,
) -> Optional[Union[GROUP_WATCH_LIST, SELF_WATCH_LIST]]:
    """获取关注列表"""
    watch_list_path = GROUP_WATCH_LIST_PATH if group else SELF_WATCH_LIST_PATH
    if watch_list_path.exists():
        with watch_list_path.open('r', encoding='utf-8') as f:
            return load(f)
    return None


def add_watch_list(
    target_id: Union[int, str],
    city_id: str,
    group: bool = True,
) -> None:
    """添加关注"""
    target_id = str(target_id)
    watch_list = get_watch_list(group)
    if watch_list is None:
        watch_list = {}
    if target_id not in watch_list:
        watch_list[target_id] = [city_id] if group else city_id
    else:
        if group:
            if city_id in watch_list[target_id]:
                raise CityInWatchListError
            watch_list[target_id].append(city_id)
        else:
            if watch_list[target_id] == city_id:
                raise CityInWatchListError
            watch_list[target_id] = city_id
    watch_list_path = GROUP_WATCH_LIST_PATH if group else SELF_WATCH_LIST_PATH
    with watch_list_path.open('w', encoding='utf-8') as f:
        dump(watch_list, f)


def remove_watch_list(
    target_id: Union[int, str],
    city_id: str,
    group: bool = True,
) -> None:
    """移除关注"""
    target_id = str(target_id)
    watch_list = get_watch_list(group)
    if watch_list is None:
        watch_list = {}
    if target_id not in watch_list:
        raise CityNotInWatchListError
    if group:
        if city_id not in watch_list[target_id]:
            raise CityNotInWatchListError
        watch_list[target_id].remove(city_id)
    else:
        if watch_list[target_id] != city_id:
            raise CityNotInWatchListError
        watch_list[target_id] = ''
    watch_list_path = GROUP_WATCH_LIST_PATH if group else SELF_WATCH_LIST_PATH
    with watch_list_path.open('w', encoding='utf-8') as f:
        dump(watch_list, f)


def get_watched_city(
    target_id: Union[int, str],
    group: bool = True,
) -> Optional[Union[List[str], str]]:
    """获取关注的城市"""
    target_id = str(target_id)
    watch_list = get_watch_list(group)
    if watch_list is None:
        return None
    if target_id not in watch_list:
        return None
    return watch_list[target_id]
