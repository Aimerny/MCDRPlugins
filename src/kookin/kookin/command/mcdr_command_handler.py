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
    if event.identified_username in config.admins or event.channel_id in config.admin_channel:
        command = ' '.join(msg)
        server.execute_command(command)
        kookApi.reply(event, command + '已执行')
    else:
        kookApi.reply(event, '仅管理员允许操作')
