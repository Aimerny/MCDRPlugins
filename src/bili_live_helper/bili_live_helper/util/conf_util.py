from mcdreforged.api.all import *

from bili_live_helper.plugin_context import PluginContext


def save_data():
    ctx = PluginContext.get()
    ctx.mcdr_server.save_config_simple(ctx.mcdr_data, ctx.mcdr_config.data_file_path)


def save_config():
    ctx = PluginContext.get()
    ctx.mcdr_server.save_config_simple(ctx.mcdr_config)