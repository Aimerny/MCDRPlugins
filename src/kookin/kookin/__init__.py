from mcdreforged.info_reactor.info import Info
from mcdreforged.api.all import *

import kook_api
import kookin.command
import kookin.util
import kookin.listener as listener
from kookin.listener import on_message

from kookin.config import Config, Data
from kookin.constant import DATA_FILE

kookApi: kook_api.KookApi
config: Config
data: Data


def on_load(server: PluginServerInterface, old_plg):
    global kookApi, config, data
    config = server.load_config_simple(target_class=Config)
    data = server.load_config_simple(
        file_name=DATA_FILE, target_class=Data
    )
    kookApi = server.get_plugin_instance('kook_api').get_api()
    server.logger.info('Kook api loaded')
    # 初始化工具模块
    util.init(config, kookApi, data)
    # 注册插件指令
    kookin.command.register(server)
    server.logger.debug('Command registered')
    # 监听API事件
    server.register_event_listener('kook_api.on_message', on_message)
    # 初始化监听Kook事件模块
    listener.init()


def on_server_startup(server: PluginServerInterface):
    util.send_to_all_channel(f'**[{config.server_name}]** is startup')


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        util.send_to_all_channel(f'**[{config.server_name}]** is stopped')
    else:
        util.send_to_all_channel(f'Is **[{config.server_name}]** crash? Server exit code is {server_return_code}')


def on_user_info(server: PluginServerInterface, info):
    if info.is_player:
        # 所有信息都会发到同步频道中
        if not info.content.startswith("!!kk"):
            util.send_to_sync_channel(
                f"<{info.player}>{info.content}"
            )


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    # 玩家加入游戏，发送到主频道+同步频道
    util.send_to_sync_channel(f'*{player} joined {config.server_name}*')
    util.send_to_public_channel(f'*{player} joined {config.server_name}*')


def on_player_left(server: PluginServerInterface, player: str):
    # 玩家离开游戏，发送到主频道+同步频道
    util.send_to_sync_channel(f'*{player} left {config.server_name}*')
    util.send_to_public_channel(f'*{player} left {config.server_name}*')
