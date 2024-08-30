import asyncio
import threading
from typing import Dict
from mcdreforged.api.all import *
from asyncio import AbstractEventLoop, Queue
from threading import Event

from bili_live_helper.bili.live_listener import LiveListener
from bili_live_helper.config.live_config import LiveConfig
from bili_live_helper.config.config import Config
from bili_live_helper.plugin_context import PluginContext


class BiliManager:
    __server: PluginServerInterface
    __logger: MCDReforgedLogger
    __config: Config
    __live_configs: Dict[str, LiveConfig]

    __async_thread: threading.Thread
    __submit_queue: Queue
    __stop_event: Event
    __event_loop: AbstractEventLoop
    __running_listener: Dict[str, LiveListener]

    def __init__(self, ctx: PluginContext):
        self.__server = ctx.mcdr_server
        self.__logger = ctx.mcdr_logger
        self.__live_configs = ctx.mcdr_data.lives
        self.__config = ctx.mcdr_config

    def start(self):
        self.__event_loop = asyncio.new_event_loop()
        self.__submit_queue = Queue(maxsize=20)
        self.__stop_event = Event()
        self.__running_listener = {}
        self.__async_thread = threading.Thread(target=self.start_event_loop, name='bili-live-listener')
        self.__async_thread.start()
        self.__logger.info('bili-live-listener thread started')

    def stop(self):
        self.__stop_event.set()
        self.__async_thread.join()

    def start_event_loop(self):
        loop = self.__event_loop
        asyncio.set_event_loop(loop)
        try:
            self.__logger.info('bili-live-listener event loop start')
            loop.run_until_complete(self.process_queue())
        finally:
            self.__logger.info('bili-live-listener event loop stopped')
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            loop.close()

    async def process_queue(self):
        self.__logger.info(f"__event_loop:{self.__event_loop}")
        while not self.__stop_event.is_set() or not self.__submit_queue.empty():
            try:
                (player, option) = await asyncio.wait_for(self.__submit_queue.get(), timeout=0.5)
                live_config = self.__live_configs.get(player)
                print(live_config)
                if live_config is not None and live_config.enable:
                    if option == 'run':
                        listener = await asyncio.create_task(self.run_listener(live_config.room_id, live_config.send_enable))
                        self.__running_listener[player] = listener
                    elif option == 'kill':
                        await asyncio.create_task(self.kill_listener(player))
                self.__submit_queue.task_done()
            except asyncio.TimeoutError:
                continue

    async def run_listener(self, room_id: int, send_enable: bool) -> LiveListener:
        self.__logger.info('run listener')
        listener = LiveListener(room_id=room_id, logger=self.__logger, **self.__config.account.__dict__)
        if send_enable:
            listener.send_enable = True
        listener.start()
        return listener

    async def kill_listener(self, player: str):
        target_listener = self.__running_listener.get(player)
        if target_listener is not None:
            await target_listener.stop()
            del self.__running_listener[player]
            self.__logger.info(f'bili-live-listener for {player} is stopped')
            return
        self.__logger.error(f'bili-live-listener for {player} not found')

    def submit(self, player: str, option: str):
        self.__submit_queue.put_nowait((player, option))
        self.__logger.info(f'Task submitted: {(player, option)}')