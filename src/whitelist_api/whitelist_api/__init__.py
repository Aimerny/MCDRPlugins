import hashlib
from typing import List
from uuid import UUID

from mcdreforged.api.all import *

from whitelist_api.api import WhitelistApi, PlayerInfo

__api: WhitelistApi
__psi: PluginServerInterface


class WhitelistException(Exception):
    def __init__(self, msg):
        super().__init__(msg)


def get_whitelist() -> List[PlayerInfo]:
    return __api.whitelist


def get_whitelist_uuids() -> List[str]:
    return [player.uuid for player in __api.whitelist]


def get_whitelist_names() -> List[str]:
    return [player.name for player in __api.whitelist]


def add_player(player: str):
    if __api.online_mode:
        add_online_player(player)
    else:
        add_offline_player(player)


def add_offline_player(player: str):
    players = get_whitelist_names()
    if player in players:
        raise WhitelistException(f"{player} is already exist")
    __api.whitelist.append(PlayerInfo(player, generate_offline_uuid(player)))
    __api.save_whitelist()
    __psi.execute('whitelist reload')


def add_online_player(player: str):
    players = get_whitelist_names()
    if player in players:
        raise WhitelistException(f"{player} is already exist")
    __psi.execute(f'whitelist add {player}')


def remove_player(player: str):
    players = get_whitelist_names()
    if player not in players:
        raise WhitelistException(f"{player} is not exist")
    __api.remove_player(player)
    __psi.execute('whitelist reload')


def enable_whitelist():
    __psi.execute('whitelist on')


def disable_whitelist():
    __psi.execute('whitelist off')


def on_load(server: PluginServerInterface, prev_module):
    global __api, __psi
    __psi = server
    __api = WhitelistApi(server.get_mcdr_config()['working_directory'], server.logger)


def on_unload(server: PluginServerInterface):
    __api.stop_watchdog()


def on_server_start(server: PluginServerInterface):
    mode = __api.refresh_online_mode()
    server.logger.warning(f'server online mode is: {mode}')


def whitelist_api():
    return __api


def generate_offline_uuid(name: str) -> str:
    def add_uuid_stripes(s):
        return str(UUID(s))

    string = "OfflinePlayer:" + name
    ha = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in ha]
    byte_array[6] = ha[6] & 0x0f | 0x30
    byte_array[8] = ha[8] & 0x3f | 0x80
    hash_modified = bytes(byte_array)
    return add_uuid_stripes(hash_modified.hex())
