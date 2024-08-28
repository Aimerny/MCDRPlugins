from mcdreforged.api.all import *

from kook_api import KookApi
from kook_api.event import Event
from kookin.config import Config, Data
from kookin.command import help_msg, bind_help_msg

config: Config
data: Data
kookApi: KookApi


def init(config_, data_, kook_api_):
    global config, data, kookApi
    config = config_
    data = data_
    kookApi = kook_api_


def handle(server: PluginServerInterface, command: str, event: Event):
    if command == 'help':
        kookApi.reply(event, help_msg)
    elif command == 'bind':
        kookApi.reply(event, bind_help_msg)
    elif command == 'whitelist':
        # todo whitelist help
        pass
    elif command == 'list':
        player_list = server.get_plugin_instance("online_player_api").get_player_list()
        message = ''
        bot_group = list(filter(lambda p: p.lower().startswith('bot_'), player_list))
        player_group = list(filter(lambda p: not p.lower().startswith('bot_'), player_list))
        if len(player_list) != 0:
            message += "=== 玩家列表 ===\n"
        for player in player_group:
            message += f'{player}\n'
        message += "=== BOT列表 ===\n"
        for bot in bot_group:
            message += f'{bot}\n'
        message += f"**在线玩家共{len(player_list)}人**\n"
        kookApi.reply(event, message)
