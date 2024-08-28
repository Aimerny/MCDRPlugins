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
    exist_user = data.find_user_by_id(event.author_id)
    if exist_user is not None:
        if event.identified_username in config.admins:
            return server.say(admin_msg(f"[Kook][{exist_user.username}]{' '.join(msg)}"))
        else:
            return server.say(common_msg(f"[Kook][{exist_user.username}]{' '.join(msg)}"))
    else:
        return send_to_sync_channel(f"*你尚未绑定Id，请使用/bind <id>绑定*")
