from asyncio import sleep
from random import uniform
from typing import Union, Literal, Optional

from nonebot import NoneBot
from aiocqhttp import ActionFailed
from aiocqhttp import Event as CQEvent

from .logger import logger
from .config import SEND_MESSAGE_INTERVAL

_sending_message = False
_pending_message = []
_interval_offset = 0.1 * SEND_MESSAGE_INTERVAL


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
        if SEND_MESSAGE_INTERVAL:
            await sleep(
                uniform(
                    SEND_MESSAGE_INTERVAL - _interval_offset,
                    SEND_MESSAGE_INTERVAL + _interval_offset,
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
    if ev is None and target_id is None:
        raise Exception('未指定目标！')
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
