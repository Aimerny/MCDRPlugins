import json

import math
import re
from typing import List
from mcdreforged.api.all import *
import datetime

__mcdr_server: PluginServerInterface
data: dict

help_msg = '''-------- §a Player Last Play §r--------
§b!!plp help §f- §c显示帮助消息
§b!!plp list [index] §f- §c显示玩家列表,index代表页数
§b!!plp get <player> §f- §c获取玩家的最后游玩时间
§b!!plp clean <player> §f- §c清除玩家的信息
-----------------------------------
'''


class Config(Serializable):
    # 一周内没上线属于很活跃
    active: int = 7
    # 两周内没上线属于较为一般
    normal: int = 14
    # 三周内没上线属于基本不活跃,超过三周属于潜水
    inactive: int = 21
    # 是否倒序查询,默认从近到远
    reverse: bool = True
    # 分页查询的大小,默认10
    pageSize: int = 10
    # 忽略玩家正则列表
    ignorePlayerRegexes: List[str] = ['^bot_.*$', '^Bot_.*$']
    # 是否只统计白名单内玩家
    only_whitelist_player: bool = False


config: Config


class PlayerInfo:
    player: str
    last_date: datetime
    activity: str

    def __init__(self, player, last_date):
        self.player = player
        self.last_date = last_date
        self.activity = self.get_activity()

    def get_activity(self) -> str:
        now = datetime.datetime.now()
        days = (now - self.last_date).days

        if days < config.active:
            return 'active'
        elif config.active <= days < config.normal:
            return 'normal'
        elif config.normal <= days < config.inactive:
            return 'inactive'
        else:
            # (这么久不上线，给红的)
            return 'danger'


def on_load(server: PluginServerInterface, old):
    # 获取存量数据
    global config, data, __mcdr_server
    __mcdr_server = server
    config = server.load_config_simple(target_class=Config)
    data = server.load_config_simple(
        'data.json',
        default_config={'player_list': {}},
        echo_in_console=True
    )['player_list']
    server.register_help_message('!!plp', '获取玩家最后一次游玩时间')

    # 注册指令
    command_builder = SimpleCommandBuilder()
    command_builder.command('!!plp list', player_list)
    command_builder.command('!!plp list <index>', player_list)
    command_builder.command('!!plp get <player>', get_player)
    command_builder.command('!!plp clean <player>', clean_player)
    command_builder.command('!!plp help', help_info)
    command_builder.command('!!plp', help_info)
    command_builder.arg('player', Text)
    command_builder.arg('index', Integer)
    command_builder.register(server)


def on_player_left(server: PluginServerInterface, player: str):
    if (is_ignore_player(player, config.ignorePlayerRegexes) or
            (config.only_whitelist_player and player not in get_whitelist_player())):
        return
    now = datetime.datetime.now().strftime('%Y-%m-%d')
    data[player] = now

    server.logger.debug(f'player {player} last play time updated!!')
    save_data(server)


# -------------------------
# command handlers
# -------------------------
def help_info(server):
    for line in help_msg.splitlines():
        server.reply(line)


def is_ignore_player(player: str, ignore_regex_list: List[str]) -> bool:
    for regex in ignore_regex_list:
        match = re.match(regex, player)
        if match is not None:
            return True
    return False


def player_list(source: CommandSource, context):
    if 'index' in context:
        index = context['index'] - 1
    else:
        index = 0
    if index < 0:
        return source.reply("查询页数不能小于1")
    pagesize = config.pageSize
    resp = RTextList('------ 玩家列表 ------\n')
    online_players = get_online_players()
    online_result_list = []
    offline_result_list = []
    result_list = []
    # 先统计在线的玩家
    for player in online_players:
        # 跳过假人
        if not is_ignore_player(player, config.ignorePlayerRegexes):
            online_result_list.append((player, '在线', RColor.green))

    # 作排序，按日期从近到远排序
    offline_players = []
    for player in data:
        # 只统计不在线的玩家
        if player not in online_players:
            offline_players.append(PlayerInfo(player, datetime.datetime.strptime(data[player], '%Y-%m-%d')))

    sorted_off_players = sort_date(offline_players)
    for player in sorted_off_players:
        # 按游玩先后顺序排序
        offline_result_list.append(
            (player.player, player.last_date.strftime("%Y-%m-%d"), get_color_by_activity(player.activity)))
    # 查分页
    result_list.extend(online_result_list)
    result_list.extend(offline_result_list)
    total = len(result_list)
    if total == 0:
        resp.append(RText('<<< 第0页/共0页 >>>'))
    else:
        pages = math.ceil(total / pagesize)
        if 0 <= index < pages - 1:
            cur_page = result_list[index * pagesize: (index + 1) * pagesize]
        elif index == pages - 1:
            cur_page = result_list[index * pagesize:]
        else:
            # 大于最大的pages
            return source.reply('超过总页数,无法查询')

        def convert_to_rtext(player_name, time, color):
            time_delta = calc_time_delta(time)
            if time_delta > 0:
                return RText(f'|-> {player_name}:{time}({time_delta}天未上线)\n', color=color)
            return RText(f'|-> {player_name}:{time}\n', color=color)

        for player_tuple in cur_page:
            resp.append(convert_to_rtext(player_tuple[0], player_tuple[1], player_tuple[2]))
        resp.append(RTextList(
            RText('<<<', color=RColor.white).h('上一页').c(RAction.run_command, f'!!plp list {index}'),
            RText(f'第{index + 1}页/共{pages}页'),
            RText('>>>', color=RColor.white).h('下一页').c(RAction.run_command, f'!!plp list {index + 2}')
        ).set_color(RColor.gray))
    source.reply(resp)


def get_player(source, context):
    player = context['player']
    online_players = get_online_players()
    if player in online_players:
        resp = RText(f'玩家{player}当前在线').set_color(RColor.green)
    elif player in data:
        player_info = PlayerInfo(player, datetime.datetime.strptime(data[player], '%Y-%m-%d'))
        resp = RText(f'玩家{player}最近的游玩时间为{data[player]}').set_color(
            get_color_by_activity(player_info.get_activity()))
    else:
        resp = RText(f'当前没有玩家{player}的游玩时间').set_color(RColor.yellow)
    source.reply(resp)


def clean_player(source, context):
    if __mcdr_server.get_permission_level(source) < 3:
        resp = RText('你没有权限清除玩家的最近游玩时间').set_color(RColor.red)
        return source.reply(resp)
    player = context.get('player')
    if player in data:
        del data[player]
        resp = RText(f'已清除玩家{player}最近的游玩时间').set_color(RColor.green)
    else:
        resp = RText(f'当前没有玩家{player}的游玩时间').set_color(RColor.red)
    source.reply(resp)


# -------------------------
# utils
# -------------------------

def save_data(server: PluginServerInterface):
    server.save_config_simple({'player_list': data}, 'data.json')


def get_online_players() -> list:
    online_player_api = __mcdr_server.get_plugin_instance('online_player_api')
    return online_player_api.get_player_list()


def sort_date(players: List[PlayerInfo]) -> List[PlayerInfo]:
    sorted_player_list = sorted(players, key=lambda player: player.last_date.timestamp(), reverse=config.reverse)
    return sorted_player_list


def get_whitelist_player() -> List[str]:
    mcdr_config = __mcdr_server.get_mcdr_config()
    server_path = mcdr_config.get('working_directory')
    whitelist_path = f'{server_path}/whitelist.json'

    whitelist = []
    with open(whitelist_path, 'r', encoding='UTF-8') as f:
        whitelist_json = json.load(f)
    for player in whitelist_json:
        whitelist.append(player['name'])
    return whitelist


def calc_time_delta(last_time_str: str):
    if last_time_str == '在线':
        return 0
    last_time = datetime.datetime.strptime(last_time_str, '%Y-%m-%d')
    now = datetime.datetime.now()
    return (now - last_time).days


def get_color_by_activity(activity: str) -> RColor:
    if activity == 'active':
        # 绿色
        return RColor.green
    elif activity == 'normal':
        # 黄色
        return RColor.yellow
    elif activity == 'inactive':
        # 红色
        return RColor.red
    else:
        # 灰色
        return RColor.gray
