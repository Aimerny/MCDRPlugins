import asyncio
import logging
from typing import Union

from bilibili_api.live import LiveDanmaku, LiveRoom
from bilibili_api import Credential
from bili_live_helper.bili.event_handler import EventHandler
from bili_live_helper.bili.live_event import LiveEvent


class LiveListener:
    __monitor: LiveDanmaku
    __sender: LiveRoom
    __handler: EventHandler
    __send_enable: bool
    __logger: logging.Logger

    @property
    def send_enable(self):
        return self.__send_enable

    @send_enable.setter
    def send_enable(self, can_send: bool):
        self.__send_enable = can_send

    @property
    def handler(self):
        return self.__handler

    @handler.setter
    def handler(self, handler: EventHandler):
        self.__handler = handler

    def __init__(self, room_id: int, uid: int, logger: logging.Logger, sessdata: str, bili_jct: str, buvid3: str,
                 ac_time_value: Union[str, None], handler: EventHandler = None):
        self.__room_id = room_id
        self.__uid = uid
        self._credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3, ac_time_value=ac_time_value)
        self.__monitor = LiveDanmaku(room_id, credential=self._credential)
        self.__sender = LiveRoom(room_id, credential=self._credential)
        self.__handler = handler

        # inject logger
        self.__logger = logger

    def start(self):
        @self.__monitor.on('DANMU_MSG')
        async def process(event):
            if self.__handler is None:
                self.__logger.warning(f'handle event failed. no event handler provided! listener: {self.__room_id}')
                return
            live_event = LiveEvent.parse_from(event)
            self.__logger.info(f'{live_event}')
            self.__handler.handle_event(live_event)

        asyncio.create_task(self.__monitor.connect())

    def stop(self):
        asyncio.create_task(self.__monitor.disconnect())
