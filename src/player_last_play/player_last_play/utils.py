import json
import re
from datetime import datetime
from pathlib import Path
from typing import List, Dict

from mcdreforged.api.all import PluginServerInterface

from player_last_play.models import PlayerInfo, PlayerRecord
from player_last_play.config import Config


def is_ignore_player(player: str, ignore_regex_list: List[str]) -> bool:
    """检查玩家是否应该被忽略"""
    return any(re.match(regex, player) is not None for regex in ignore_regex_list)


def get_whitelist_players(server: PluginServerInterface) -> List[str]:
    """获取白名单玩家列表"""
    mcdr_config = server.get_mcdr_config()
    server_path = mcdr_config.get('working_directory')
    whitelist_path = Path(server_path) / 'whitelist.json'

    with open(whitelist_path, 'r', encoding='UTF-8') as f:
        whitelist_json = json.load(f)
    return [player['name'] for player in whitelist_json]


def get_online_players(server: PluginServerInterface) -> List[str]:
    """获取在线玩家列表"""
    online_player_api = server.get_plugin_instance('online_player_api')
    return online_player_api.get_player_list()


def load_player_data(server: PluginServerInterface) -> Dict[str, PlayerRecord]:
    """加载玩家数据"""
    data = server.load_config_simple(
        'data.json',
        default_config={'player_list': {}},
        echo_in_console=True
    )['player_list']
    result: Dict[str, PlayerRecord] = {}
    for player, raw in data.items():
        if isinstance(raw, str):
            # Legacy format that only stored the last date
            last_date = datetime.strptime(raw, '%Y-%m-%d')
            result[player] = PlayerRecord(last_date=last_date)
        elif isinstance(raw, dict):
            last_raw = raw.get('last_date') or raw.get('last_seen')
            if not last_raw:
                continue
            last_date = datetime.strptime(last_raw, '%Y-%m-%d')
            total_seconds = int(raw.get('total_seconds', 0))
            result[player] = PlayerRecord(last_date=last_date, total_seconds=total_seconds)
        else:
            continue
    return result


def save_player_data(server: PluginServerInterface, data: Dict[str, PlayerRecord]) -> None:
    """保存玩家数据"""
    formatted_data = {
        player: {
            'last_date': record.last_date.strftime('%Y-%m-%d'),
            'total_seconds': record.total_seconds
        }
        for player, record in data.items()
    }
    server.save_config_simple({'player_list': formatted_data}, 'data.json')


def create_player_info(name: str, record: PlayerRecord, config: Config) -> PlayerInfo:
    """创建PlayerInfo实例"""
    return PlayerInfo(name=name, record=record, config=config)


def sort_players(players: List[PlayerInfo], reverse: bool = True) -> List[PlayerInfo]:
    """按最后游玩时间排序玩家列表"""
    return sorted(players, key=lambda p: p.record.last_date.timestamp(), reverse=reverse)
