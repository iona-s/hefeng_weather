from asyncio import sleep
from random import uniform
from typing import Union, Literal, Optional

from nonebot import NoneBot
from aiocqhttp import ActionFailed
from aiocqhttp import Event as CQEvent

from .config import config
from .logger import logger

_sending_message = False
_pending_message = []
if config.SEND_MESSAGE_INTERVAL:
    _interval_offset = 0.1 * config.SEND_MESSAGE_INTERVAL
    _interval = (
        config.SEND_MESSAGE_INTERVAL - _interval_offset,
        config.SEND_MESSAGE_INTERVAL + _interval_offset,
    )
else:
    _interval = None


async def _send_message(
    bot: NoneBot,
    message: str,
    *,
    ev: Optional[CQEvent] = None,
    target_type: Literal['group', 'private'] = 'group',
    target_id: Optional[Union[int, str]] = None,
):
    try:
        if ev is not None:
            await bot.send(ev, message)
        elif target_type == 'group':
            await bot.send_group_msg(group_id=int(target_id), message=message)
        elif target_type == 'private':
            await bot.send_private_msg(user_id=int(target_id), message=message)
    except ActionFailed:
        target = ev.group_id if ev.group_id else target_id
        logger.error(f'向{target}发送消息{message}失败')


async def _run_pending_tasks():
    global _sending_message
    global _pending_message
    if _sending_message:
        return
    _sending_message = True
    while _pending_message:
        await _pending_message.pop(0)
        if _interval is not None:
            await sleep(
                uniform(
                    *_interval,
                ),
            )
    _sending_message = False


async def bot_send(
    bot: NoneBot,
    message: str,
    *,
    ev: Optional[CQEvent] = None,
    target_type: Literal['group', 'private'] = 'group',
    target_id: Optional[Union[int, str]] = None,
):
    """bot发送消息的封装，用于控制消息发送频率，现在已意义不大"""
    if ev is None and target_id is None:
        error_msg = '发送消息未指定目标！'
        raise AssertionError(error_msg)
    _pending_message.append(
        _send_message(
            bot,
            message,
            ev=ev,
            target_type=target_type,
            target_id=target_id,
        ),
    )
    await _run_pending_tasks()
