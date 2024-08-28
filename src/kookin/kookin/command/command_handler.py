from kook_api.event import Event
from kookin.util import *
from mcdreforged.api.all import *

config: Config
data: Data
kookApi: KookApi


def init(config_, data_, kook_api_):
    global config, data, kookApi
    config = config_
    data = data_
    kookApi = kook_api_


def handle(server: PluginServerInterface, command_nodes: List[str], event: Event):
    msg = command_nodes[1:]
    if event.identified_username in config.admins or event.channel_id in get_all_admin_channel_ids():
        resp = server.rcon_query(' '.join(msg))
        if server.is_rcon_running():
            kookApi.reply(event, resp)
        else:
            kookApi.reply(event, '指令已执行,未开启RCON无结果')
    else:
        kookApi.reply(event, '仅管理员允许操作')
