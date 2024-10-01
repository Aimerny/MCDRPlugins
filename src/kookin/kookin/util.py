import re
from typing import List

from mcdreforged.api.all import *

from kookin import PluginContext


def save_data():
    ctx = PluginContext.get()
    ctx.mcdr_server.save_config_simple(ctx.mcdr_data, ctx.mcdr_config.data_file_path)


def save_config():
    ctx = PluginContext.get()
    ctx.mcdr_server.save_config_simple(ctx.mcdr_config)

# === Config Var ===
def get_all_public_channel_ids() -> List[str]:
    return convert_channel_list_to_ids(PluginContext.get().mcdr_config.public_channel)


def get_all_sync_chat_channel_ids() -> List[str]:
    return convert_channel_list_to_ids(PluginContext.get().mcdr_config.sync_chat_channel)


def get_all_admin_channel_ids() -> List[str]:
    return convert_channel_list_to_ids(PluginContext.get().mcdr_config.admin_channel)


def convert_channel_list_to_ids(channels: List[dict]) -> List[str]:
    channel_ids = []
    for channel_info in channels:
        channel_ids.append(channel_info['channel_id'])
    return channel_ids