from mcdreforged.api.all import *

from kook_api.config import Config
from kook_api.api import KookApi
from kook_api import serve

config: Config
api: KookApi


def on_load(server: PluginServerInterface, old_plg):
    global config, api
    config = server.load_config_simple(target_class=Config)
    api = KookApi(mcdr_server=server, api_host=config.kook_host, api_port=config.api_port)
    serve.start(server, config)


def on_unload(server: PluginServerInterface):
    serve.stop(server)


def get_api() -> KookApi:
    return api
