from mcdreforged.api.all import *

from offline_whitelist_reforged.Config import Config
from offline_whitelist_reforged.plugin import Plugin

plugin: Plugin
config: Config


def on_load(server: PluginServerInterface, old):
    global plugin, config
    config = server.load_config_simple(target_class=Config)
    plugin = Plugin(server, config)
