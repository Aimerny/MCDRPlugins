from mcdreforged.command.builder.nodes.arguments import GreedyText
from mcdreforged.command.builder.nodes.basic import Literal
from mcdreforged.api.all import *

import kookin.util as util
from kook_api.event import Event
from kookin.config import Config
from kookin.constant import GlobalKey

config: Config

help_msg = \
    f"""\
======= KookIn =======
/bind      =>   成员绑定
/whitelist => 白名单管理
/list      =>   在线列表
/help      =>   查询指令
=======  Help  =======
"""

bind_help_msg = \
    f"""\
======= KookIn ========
/bind <mc_id> => 绑定MC
/bind clear @ => 清除指定用户绑定信息
/bind list    => 已绑定列表
=======  Bind  ========
"""


def command_parse(event: Event):
    content = event.content
    channel_id = event.channel_id

    # 同步频道的消息转到服务器
    if channel_id in config.sync_chat_channel:
        util.send_to_sync_channel(content)


def register(server: PluginServerInterface):
    global config
    config = util.get_global(GlobalKey.config)
    # register MCDR command
    server.register_command(
        Literal("!!kk").then(GreedyText("message").runs(send_message))
    )
    server.register_command(
        Literal("!!kkchans").then(GreedyText("search_key").runs(search_chans)).runs(get_all_chans)
    )


def send_message(server, ctx):
    player = server.player if server.is_player else "Server"
    message = f'<{player}>{ctx["message"]}'
    util.send_to_sync_channel(message)
    util.send_to_public_channel(message)


def get_all_chans(server: PluginServerInterface, ctx):
    search_chans(server, ctx)


def search_chans(server, ctx: dict):
    guilds_group = {}
    res_content = '----- channels list -----\n'
    search_key = ''
    if 'search_key' in ctx:
        search_key = ctx['search_key']
    channels = util.search_channels(search_key)
    # server.logger().debug(f"searched channels : {channels}")
    for channel in channels:
    #     if channel["guild_id"] in guilds_group.keys():
    #         guilds_group[channel["guild_id"]] = []
    #     guilds_group[channel["guild_id"]].append(channel)
    #
    # for grouped_channels in guilds_group.values():
    #     if len(grouped_channels) == 0:
    #         continue
    #     res_content += f'---- {grouped_channels[0].guild_name} ----\n'
    #     for channel in grouped_channels:
        res_content += f'[{channel["guild_name"]}]=>[{channel["channel_name"]}]=>[{channel["channel_id"]}]\n'
    res_content += '----------------------'
    server.reply(res_content)
