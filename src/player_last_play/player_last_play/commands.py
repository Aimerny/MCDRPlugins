import math
from datetime import datetime
from typing import List, Tuple, Optional

from mcdreforged.api.all import *

from player_last_play.config import Config
from player_last_play.models import PlayerInfo
from player_last_play.utils import (
    get_online_players, is_ignore_player, get_whitelist_players,
    load_player_data, save_player_data, create_player_info, sort_players
)


class CommandManager:

    def __init__(self, server: PluginServerInterface, config: Config):
        self.server = server
        self.config = config
        self.data = load_player_data(server)
        self._register_commands()

    def _register_commands(self) -> None:
        """注册所有命令"""
        builder = SimpleCommandBuilder()
        builder.command('!!plp list', self.list_players)
        builder.command('!!plp list <index>', self.list_players)
        builder.command('!!plp get <player>', self.get_player)
        builder.command('!!plp clean <player>', self.clean_player)
        builder.command('!!plp help', self.show_help)
        builder.command('!!plp', self.show_help)
        builder.arg('player', Text)
        builder.arg('index', Integer)
        builder.register(self.server)

    def show_help(self, source: CommandSource) -> None:
        """显示帮助信息"""
        help_msg = RTextList()
        (help_msg.append('--------', RText(' Player Last Play ', color=RColor.green), '--------', '\n')
                .append(RText('!!plp help', color=RColor.green).c(RAction.run_command, '!!plp help'), ' - ', RText('显示帮助信息', color=RColor.red), '\n')
                .append(RText('!!plp list [index]', color=RColor.green).c(RAction.suggest_command, '!!plp list '), ' - ', RText('显示玩家列表, index代表页数', color=RColor.red), '\n')
                .append(RText('!!plp get <player>', color=RColor.green).c(RAction.suggest_command, '!!plp get '), '-', RText('获取玩家的最后游玩时间', color=RColor.red), '\n')
                .append(RText('!!plp clean <player>', color=RColor.green).c(RAction.suggest_command, '!!plp clean '), '-', RText('清楚玩家的游玩时间信息', color=RColor.red), '\n')
                .append('-----------------------------------')
        )
        source.reply(help_msg)
        

    def list_players(self, source: CommandSource, context: dict) -> None:
        """列出玩家列表"""
        index = context.get('index', 1) - 1
        if index < 0:
            return source.reply("查询页数不能小于1")

        online_players = get_online_players(self.server)
        result_list = self._prepare_player_list(online_players)
        
        if not result_list:
            return source.reply(RTextList('------ 玩家列表 ------\n', 
                                        RText('<<< 第0页/共0页 >>>')))

        pages = math.ceil(len(result_list) / self.config.pageSize)
        if not (0 <= index < pages):
            return source.reply('超过总页数,无法查询')

        start = index * self.config.pageSize
        end = start + self.config.pageSize
        current_page = result_list[start:end]

        resp = RTextList('------ 玩家列表 ------\n')
        for player, status, color in current_page:
            resp.append(self._format_player_entry(player, status, color))

        resp.append(self._create_pagination_controls(index, pages))
        source.reply(resp)

    def get_player(self, source: CommandSource, context: dict) -> None:
        """获取玩家信息"""
        player = context['player']
        online_players = get_online_players(self.server)
        
        if player in online_players:
            resp = RText(f'玩家{player}当前在线').set_color(RColor.green)
        elif player in self.data:
            player_info = create_player_info(player, self.data[player], self.config)
            resp = RText(f'玩家{player}最近的游玩时间为{self.data[player].strftime("%Y-%m-%d")}').set_color(
                player_info.activity.color)
        else:
            resp = RText(f'当前没有玩家{player}的游玩时间').set_color(RColor.yellow)
        
        source.reply(resp)

    def clean_player(self, source: CommandSource, context: dict) -> None:
        """清除玩家信息"""
        if self.server.get_permission_level(source) < 3:
            return source.reply(RText('你没有权限清除玩家的最近游玩时间').set_color(RColor.red))

        player = context['player']
        if player in self.data:
            del self.data[player]
            save_player_data(self.server, self.data)
            resp = RText(f'已清除玩家{player}最近的游玩时间').set_color(RColor.green)
        else:
            resp = RText(f'当前没有玩家{player}的游玩时间').set_color(RColor.red)
        
        source.reply(resp)

    def update_player_time(self, player: str) -> None:
        """更新玩家最后游玩时间"""
        if (is_ignore_player(player, self.config.ignorePlayerRegexes) or
                (self.config.only_whitelist_player and 
                 player not in get_whitelist_players(self.server))):
            return

        self.data[player] = datetime.now()
        save_player_data(self.server, self.data)
        self.server.logger.debug(f'player {player} last play time updated!!')

    def _prepare_player_list(self, online_players: List[str]) -> List[Tuple[str, str, RColor]]:
        """准备玩家列表数据"""
        result_list = []
        
        # 添加在线玩家
        for player in online_players:
            if not is_ignore_player(player, self.config.ignorePlayerRegexes):
                result_list.append((player, '在线', RColor.green))

        # 添加离线玩家
        offline_players = []
        for player, last_date in self.data.items():
            if player not in online_players:
                player_info = create_player_info(player, last_date, self.config)
                offline_players.append(player_info)

        sorted_players = sort_players(offline_players, self.config.reverse)
        for player in sorted_players:
            result_list.append((
                player.name,
                player.last_date.strftime("%Y-%m-%d"),
                player.activity.color
            ))

        return result_list

    def _format_player_entry(self, player: str, time_str: str, color: RColor) -> RText:
        """格式化玩家条目"""
        if time_str == '在线':
            return RText(f'|-> {player}:{time_str}\n', color=color)
        
        days = (datetime.now() - datetime.strptime(time_str, '%Y-%m-%d')).days
        return RText(f'|-> {player}:{time_str}({days}天未上线)\n', color=color)

    def _create_pagination_controls(self, current_page: int, total_pages: int) -> RTextList:
        """创建分页控制"""
        return RTextList(
            RText('<<<', color=RColor.white)
            .h('上一页')
            .c(RAction.run_command, f'!!plp list {current_page}'),
            RText(f'第{current_page + 1}页/共{total_pages}页'),
            RText('>>>', color=RColor.white)
            .h('下一页')
            .c(RAction.run_command, f'!!plp list {current_page + 2}')
        ).set_color(RColor.gray) 