from mcdreforged.api.all import *

import asyncio
import logging
import threading
from kookin.api.command_handler import HelpCommandHandler, McCommandHandler, ExecuteCommandHandler, \
    WhitelistCommandHandler, McdrCommandHandler, ListCommandHandler
from asyncio import AbstractEventLoop, Task
from khl import Bot, Message
from kookin.config import Config


class KookApi:
    __bot: Bot
    __config: Config
    __running: bool
    __async_thread: threading.Thread
    __server: PluginServerInterface
    __logger: logging.Logger
    __event_loop: AbstractEventLoop
    __bot_task: Task

    def __init__(self, server: PluginServerInterface, config: Config):
        if config is None or config.token == '':
            from kookin.exceptions import ConfigParseError
            raise ConfigParseError("解析配置失败,请确定token合法")
        self.__bot = Bot(token=config.token)
        self.__running = False
        self.__server = server
        self.__logger = server.logger
        self.__config = config

    def start(self):
        self.__event_loop = asyncio.new_event_loop()
        self.__async_thread = threading.Thread(target=self.start_event_loop, name='kook-api')
        self.__async_thread.start()
        self.__running = True
        self.__logger.info('kook-api thread started')

    def stop(self):
        asyncio.run_coroutine_threadsafe(self.__bot.client.offline(), self.__event_loop)
        self.__bot_task.cancel()
        self.__async_thread.join()

    def start_event_loop(self):
        loop = self.__event_loop
        asyncio.set_event_loop(loop)
        try:
            self.__logger.info('kook-api event loop started')
            self.__bot_task = self.__event_loop.create_task(self.run())
            loop.run_until_complete(self.__bot_task)
        except asyncio.CancelledError:
            self.__logger.warning('kook-api event loop stopping')
        finally:
            self.__logger.info('kook-api event loop stopped')
            pending = asyncio.all_tasks(loop)
            for task in pending:
                task.cancel()
            loop.run_until_complete(asyncio.gather(*pending, return_exceptions=True))
            loop.close()

    async def run(self):
        def all_channel_filter(message: Message) -> bool:
            import kookin.util as util
            return (message.target_id in util.get_all_admin_channel_ids()
                    or message.target_id in util.get_all_public_channel_ids()
                    or message.target_id in util.get_all_sync_chat_channel_ids())

        def sync_channel_filter(message: Message) -> bool:
            import kookin.util as util
            return message.target_id in util.get_all_sync_chat_channel_ids()

        @self.__bot.command(name="mc", prefixes=self.__config.prefixes, rules=[all_channel_filter])
        async def mc(message: Message, content: str):
            return await McCommandHandler(self.__server, self.__config).handle(message, content=content)

        # @self.__bot.command(name="bind", prefixes=self.__config.prefixes)
        async def bind(message: Message, player_name: str):
            # todo 暂时不处理,考虑是否还需要bind
            pass

        @self.__bot.command(name="whitelist", prefixes=self.__config.prefixes)
        async def whitelist(message: Message, sub_command='', player=''):
            return await WhitelistCommandHandler(self.__server, self.__config).handle(message, sub_command, player)

        @self.__bot.command(name="execute", prefixes=self.__config.prefixes)
        async def execute_command(message: Message, *args):
            return await ExecuteCommandHandler(self.__server, self.__config).handle(message, " ".join(args))

        @self.__bot.command(name="mcdr", prefixes=self.__config.prefixes)
        async def execute_mcdr(message: Message, *args):
            return await McdrCommandHandler(self.__server, self.__config).handle(message, " ".join(args))

        @self.__bot.command(name="help", prefixes=self.__config.prefixes)
        async def help_command(message: Message, secondary_command: str = ''):
            return await HelpCommandHandler(self.__server, self.__config).handle(message, sub_command=secondary_command)

        @self.__bot.command(name="list", prefixes=self.__config.prefixes)
        async def list_command(message: Message):
            return await ListCommandHandler(self.__server, self.__config).handle(message)

        @self.__bot.on_message()
        async def common_message(message: Message):
            content = message.content
            for prefix in self.__config.prefixes:
                # 如果是指令前缀就跳过
                if content.startswith(prefix):
                    return
            if sync_channel_filter(message):
                return await McCommandHandler(self.__server, self.__config).handle(message, content)

        await self.__bot.start()

    def send_text_to_channel(self, content: str, channel_id: str):
        async def send_to_channel():
            channel = await self.__bot.client.fetch_public_channel(channel_id=channel_id)
            await channel.send(content)

        asyncio.run_coroutine_threadsafe(send_to_channel(), self.__event_loop)

    def send_to_public_channel(self, content: str):
        for channel_info in self.__config.public_channel:
            self.send_text_to_channel(content, channel_info["channel_id"])

    def send_to_sync_channel(self, content: str):
        for channel_info in self.__config.sync_chat_channel:
            self.send_text_to_channel(content, channel_info["channel_id"])

    def send_to_admin_channel(self, content: str):
        for channel_info in self.__config.admin_channel:
            self.send_text_to_channel(content, channel_info["channel_id"])

    def send_to_all_channel(self, content: str):
        self.send_to_public_channel(content)
        self.send_to_sync_channel(content)
        self.send_to_admin_channel(content)
