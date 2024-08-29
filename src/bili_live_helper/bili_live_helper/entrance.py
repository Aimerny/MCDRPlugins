from mcdreforged.api.all import *

from bili_live_helper.config.config import Config
from bili_live_helper.config.data import DataConfig
from bili_live_helper.mcdr.bili_manager import BiliManager
from bili_live_helper.plugin_context import PluginContext, load_plugin_context
from bili_live_helper.mcdr.command_manager import CommandManager

bili_manager: BiliManager


def on_load(server: PluginServerInterface, old):
    global bili_manager
    server.logger.info("load bili live helper!")
    config = server.load_config_simple(target_class=Config)
    if config.data_file_path == '':
        server.logger.warning("data file path is empty! use default path 'data.json'")
        config.data_file_path = 'data.json'
    data = server.load_config_simple(target_class=DataConfig, file_name=config.data_file_path)

    # init plugin context
    plg_ctx = PluginContext(server, config, data)
    load_plugin_context(plg_ctx)

    # start bili manager
    bili_manager = BiliManager(ctx=plg_ctx)
    if plg_ctx.mcdr_config.enable:
        bili_manager.start()

    command_manager = CommandManager(ctx=plg_ctx, bili_manager=bili_manager)
    command_manager.register_command()


def on_unload(server: PluginServerInterface):
    bili_manager.stop()
    server.logger.info("unload bili live helper!")
