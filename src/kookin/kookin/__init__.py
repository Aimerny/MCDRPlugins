from mcdreforged.api.all import *

from kookin.api.kook_api import KookApi

from kookin.config import Config, Data
from kookin.plugin_context import PluginContext, load_plugin_context


def on_load(server: PluginServerInterface, old_plg):
    mcdr_config = server.load_config_simple(target_class=Config)
    data = server.load_config_simple(
        file_name='data.json', target_class=Data
    )

    kook_api = KookApi(server, mcdr_config)
    kook_api.start()
    # init plugin context
    plg_ctx = PluginContext(server, kook_api, mcdr_config, data)
    load_plugin_context(plg_ctx)

    server.logger.info('Kook api loaded')

    def send_message(source, ctx):
        player = source.player if source.is_player else "Server"
        message = f'<{player}>{ctx["message"]}'
        kook_api.send_to_public_channel(message)
        kook_api.send_to_sync_channel(message)

    # 注册插件指令
    server.register_command(
        Literal("!!kk").then(GreedyText("message").runs(send_message))
    )
    server.register_command(
        Literal("!!kook").then(GreedyText("message").runs(send_message))
    )


def on_unload(server: PluginServerInterface):
    server.logger.warning('kookin stopping')
    PluginContext.get().kook_api.stop()
    server.logger.info('kookin stopped')


def on_server_startup(server: PluginServerInterface):
    PluginContext.get().kook_api.send_to_all_channel(f'**[{PluginContext.get().mcdr_config.server_name}]** is startup')


def on_server_stop(server: PluginServerInterface, server_return_code: int):
    if server_return_code == 0:
        PluginContext.get().kook_api.send_to_all_channel(
            f'**[{PluginContext.get().mcdr_config.server_name}]** is stopped')
    else:
        PluginContext.get().kook_api.send_to_all_channel(
            f'Is **[{PluginContext.get().mcdr_config.server_name}]** crash? Server exit code is {server_return_code}')
    PluginContext.get().kook_api.stop()


def on_user_info(server: PluginServerInterface, info):
    if info.is_player:
        # 所有信息都会发到同步频道中
        if not info.content.startswith("!!kk"):
            PluginContext.get().kook_api.send_to_sync_channel(
                f"<{info.player}>{info.content}"
            )


def on_player_joined(server: PluginServerInterface, player: str, info: Info):
    # 玩家加入游戏，发送到主频道+同步频道
    PluginContext.get().kook_api.send_to_sync_channel(
        f'*{player} joined {PluginContext.get().mcdr_config.server_name}*')
    PluginContext.get().kook_api.send_to_public_channel(
        f'*{player} joined {PluginContext.get().mcdr_config.server_name}*')


def on_player_left(server: PluginServerInterface, player: str):
    # 玩家离开游戏，发送到主频道+同步频道
    PluginContext.get().kook_api.send_to_sync_channel(f'*{player} left {PluginContext.get().mcdr_config.server_name}*')
    PluginContext.get().kook_api.send_to_public_channel(
        f'*{player} left {PluginContext.get().mcdr_config.server_name}*')
