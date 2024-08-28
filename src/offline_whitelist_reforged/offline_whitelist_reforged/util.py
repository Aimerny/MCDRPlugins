import hashlib
import json
from typing import List
from uuid import UUID
from mcdreforged.api.all import *


class PlayerInfo:
    name: str
    uuid: str

    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid


def load_whitelist(server: ServerInterface) -> List[PlayerInfo]:
    mcdr_config = server.get_mcdr_config()
    server_path = mcdr_config.get('working_directory')
    whitelist_path = f'{server_path}/whitelist.json'
    whitelist = []
    with open(whitelist_path, 'r', encoding='UTF-8') as f:
        whitelist_json = json.load(f)
    for player in whitelist_json:
        whitelist.append(PlayerInfo(player['name'], player['uuid']))
    return whitelist


def save_whitelist(server: ServerInterface, whitelist: List[PlayerInfo]):
    mcdr_config = server.get_mcdr_config()
    server_path = mcdr_config.get('working_directory')
    whitelist_path = f'{server_path}/whitelist.json'
    whitelist_json = []
    for player_info in whitelist:
        whitelist_json.append({'uuid': player_info.uuid, 'name': player_info.name})
    with open(whitelist_path, 'w', encoding='UTF-8') as f:
        f.write(json.dumps(whitelist_json, indent=2, separators=(',', ':'), ensure_ascii=False))


def generate_offline_uuid(player) -> str:
    def add_uuid_stripes(s):
        return str(UUID(s))

    string = "OfflinePlayer:" + player
    ha = hashlib.md5(string.encode('utf-8')).digest()
    byte_array = [byte for byte in ha]
    byte_array[6] = ha[6] & 0x0f | 0x30
    byte_array[8] = ha[8] & 0x3f | 0x80
    hash_modified = bytes(byte_array)
    return add_uuid_stripes(hash_modified.hex())


def replace_code(msg: str) -> str:
    return msg.replace('&', '§')
