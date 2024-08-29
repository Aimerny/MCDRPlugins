import asyncio

from bilibili_api.live import LiveDanmaku, LiveRoom
from bilibili_api import Credential, Danmaku


class Listener:
    _monitor: LiveDanmaku
    _sender: LiveRoom

    def __init__(self, room_id: int, uid: int, sessdata: str, bili_jct: str, buvid3: str, ac_time_value):
        self._room_id = room_id
        self._uid = uid
        self._credential = Credential(sessdata=sessdata, bili_jct=bili_jct, buvid3=buvid3, ac_time_value=ac_time_value)
        self._monitor = LiveDanmaku(room_id, credential=self._credential)
        self._sender = LiveRoom(room_id, credential=self._credential)

    def start_listener(self):
        @self._monitor.on('DANMU_MSG')
        async def process(event):
            print(event)

        asyncio.create_task(self._monitor.connect())

    def stop_listener(self):
        asyncio.create_task(self._monitor.disconnect())
