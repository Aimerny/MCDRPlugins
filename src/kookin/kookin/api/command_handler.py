from mcdreforged.api.all import *

from enum import Enum
from typing import List, Union
from khl import Message

from kookin.config import Config
from kookin.api import help_msg
from whitelist_api import WhitelistException


class CommandEnum(Enum):
    HELP = 'help',
    WHITELIST = 'whitelist',
    LIST = 'list',
    MC = 'mc',
    MCDR = 'mcdr',
    EXECUTE = 'execute'


def check_author_admin(message: Message, config: Config) -> bool:
    import kookin.util as util
    admin_channel = util.get_all_admin_channel_ids()
    if message.target_id in admin_channel:
        return True
    unique_name = f'{message.author.username}#{message.author.identify_num}'
    if len(config.admins) > 0:
        return unique_name in config.admins
    return False


class CommandHandler:

    @property
    def server(self):
        return self.__server

    @property
    def config(self):
        return self.__config

    def __init__(self, server: 'PluginServerInterface', config: 'Config'):
        self.__server = server
        self.__config = config


class HelpCommandHandler(CommandHandler):
    async def handle(self, message: Message, sub_command: Union[str, CommandEnum] = None):
        if sub_command is None or sub_command == '':
            return await message.reply(help_msg.root_help_msg)
        # 传入字符串就转成枚举
        if isinstance(sub_command, str):
            try:
                sub_command = CommandEnum[sub_command.upper()]
            except KeyError:
                return await message.reply(f'*未找到该指令*: {sub_command}')

        if sub_command == CommandEnum.HELP:
            return await message.reply(help_msg.root_help_msg)
        elif sub_command == CommandEnum.LIST:
            return await message.reply(help_msg.list_help_msg)
        elif sub_command == CommandEnum.MC:
            return await message.reply(help_msg.mc_help_msg)
        elif sub_command == CommandEnum.MCDR:
            return await message.reply(help_msg.mcdr_help_msg)
        elif sub_command == CommandEnum.EXECUTE:
            return await message.reply(help_msg.execute_help_msg)
        elif sub_command == CommandEnum.WHITELIST:
            return await message.reply(help_msg.whitelist_help_msg)


class McCommandHandler(CommandHandler):
    async def handle(self, message: Message, content: str):
        if content == '':
            return await message.reply(help_msg.mc_help_msg)
        nickname = message.author.nickname if message.author.nickname != '' else message.author.username
        self.server.broadcast(
            RText(f'[Kook]<{nickname}> {content}').set_color(RColor.dark_green).set_styles(RStyle.italic))


class ListCommandHandler(CommandHandler):
    async def handle(self, message: Message):
        player_list = self.server.get_plugin_instance('online_player_api').get_player_list()
        bot_group = list(filter(lambda p: p.lower().startswith('bot_'), player_list))
        player_group = list(filter(lambda p: not p.lower().startswith('bot_'), player_list))
        reply_msg = ""
        if len(player_list) != 0:
            reply_msg += "=== 玩家列表 ===\n"
        for player in player_group:
            reply_msg += f'- {player}\n'
        reply_msg += "=== BOT列表 ===\n"
        for bot in bot_group:
            reply_msg += f'{bot}\n'
        reply_msg += f"**在线玩家共{len(player_list)}人**\n"
        return await message.reply(reply_msg)


class WhitelistCommandHandler(CommandHandler):
    async def handle(self, message: Message, sub_command, player_name):
        if sub_command is None or sub_command == '':
            return await message.reply(help_msg.whitelist_help_msg)
        if not check_author_admin(message, self.config):
            return await message.reply('你不是管理员,无权执行该指令')
        whitelist_api = self.server.get_plugin_instance('whitelist_api')
        if sub_command == 'on':
            whitelist_api.enable_whitelist()
            return await message.reply('已开启服务器白名单')
        elif sub_command == 'off':
            whitelist_api.disable_whitelist()
            return await message.reply('已关闭服务器白名单')
        elif sub_command == 'add':
            if player_name is None:
                return await message.reply('玩家名不能为空')
            try:
                whitelist_api.add_player(player_name)
                return await message.reply(f'已将*{player_name}*添加到白名单中')
            except WhitelistException:
                return await message.reply(f'添加失败, 玩家*{player_name}*已在白名单中')
        elif sub_command == 'rm':
            if player_name is None:
                return await message.reply('玩家名不能为空')
            try:
                whitelist_api.remove_player(player_name)
                return await message.reply(f'已将*{player_name}*从白名单移除')
            except WhitelistException:
                return await message.reply(f'移除失败, 玩家*{player_name}*不在白名单中')
        elif sub_command == 'list':
            whitelist_names = whitelist_api.get_whitelist_names()
            reply_msg = "=== 白名单列表 ===\n"
            if len(whitelist_names) > 0:
                for player in whitelist_names:
                    reply_msg += f"- {player}\n"
            reply_msg += f"白名单中玩家共计{len(whitelist_names)}人"
            return await message.reply(reply_msg)


class McdrCommandHandler(CommandHandler):
    async def handle(self, message: Message, command: str):
        if not check_author_admin(message, self.config):
            return await message.reply('你不是管理员,无权执行该指令')
        if command == '':
            return await message.reply('指令不合法')
        if not command.startswith('!!'):
            command = '!!' + command
        self.server.execute_command(command)
        return await message.reply(f'指令: {command}已执行')


class ExecuteCommandHandler(CommandHandler):
    async def handle(self, message: Message, command: str = ''):
        if not check_author_admin(message, self.config):
            return await message.reply('你不是管理员,无权执行该指令')
        resp = self.server.rcon_query(command)
        if self.server.is_rcon_running():
            if resp == '':
                return await message.reply('指令已执行,返回结果为空')
            await message.reply(resp)
        else:
            await message.reply('指令已执行,未开启RCON无结果')
