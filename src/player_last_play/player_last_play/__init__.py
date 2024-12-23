from mcdreforged.api.all import *

from player_last_play.commands import CommandManager
from player_last_play.config import Config


command_manager: CommandManager = None


def on_load(server: PluginServerInterface, old):
    global command_manager
    config = server.load_config_simple(target_class=Config)
    config.validate()  # 验证配置有效性
    
    command_manager = CommandManager(server, config)
    server.register_help_message('!!plp', '获取玩家最后一次游玩时间')


def on_player_left(server: PluginServerInterface, player: str):
    command_manager.update_player_time(player)
