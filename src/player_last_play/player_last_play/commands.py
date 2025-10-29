import math
from datetime import datetime
from typing import Dict, List, Optional, Tuple

from mcdreforged.api.all import *

from player_last_play.config import Config
from player_last_play.models import PlayerInfo, PlayerRecord
from player_last_play.utils import (
    get_online_players, is_ignore_player, get_whitelist_players,
    load_player_data, save_player_data, create_player_info, sort_players
)


class CommandManager:

    def __init__(self, server: PluginServerInterface, config: Config):
        self.server = server
        self.config = config
        self.data = load_player_data(server)
        self._session_start_times: Dict[str, datetime] = {}
        self._warm_up_online_sessions()
        self._register_commands()

    def _register_commands(self) -> None:
        """注册所有命令"""
        builder = SimpleCommandBuilder()
        builder.command('!!plp list', self.list_players)
        builder.command('!!plp list <index>', self.list_players)
        builder.command('!!plp get <player>', self.get_player)
        builder.command('!!plp clean <player>', self.clean_player)
        builder.command('!!plp reset <player>', self.reset_player_total)
        builder.command('!!plp help', self.show_help)
        builder.command('!!plp', self.show_help)
        builder.arg('player', Text)
        builder.arg('index', Integer)
        builder.register(self.server)

    def show_help(self, source: CommandSource) -> None:
        """显示帮助信息"""
        help_msg = RTextList()
        (help_msg.append('--------', RText(' Player Last Play ', color=RColor.green), '--------', '\n')
                .append(RText('!!plp help', color=RColor.green).c(RAction.run_command, '!!plp help'), ' - ',
                        RText('显示帮助信息', color=RColor.red), '\n')
                .append(RText('!!plp list [index]', color=RColor.green).c(RAction.suggest_command, '!!plp list '), ' - ',
                        RText('显示玩家列表, index代表页数', color=RColor.red), '\n')
                .append(RText('!!plp get <player>', color=RColor.green).c(RAction.suggest_command, '!!plp get '), '-',
                        RText('获取玩家的最后游玩时间与总在线时长', color=RColor.red), '\n')
                .append(RText('!!plp clean <player>', color=RColor.green).c(RAction.suggest_command, '!!plp clean '), '-',
                        RText('清除玩家的游玩时间信息', color=RColor.red), '\n')
                .append(RText('!!plp reset <player>', color=RColor.green).c(RAction.suggest_command, '!!plp reset '), '-',
                        RText('重置玩家的累计在线时长', color=RColor.red), '\n')
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
        for player, info, is_online, color in current_page:
            resp.append(self._format_player_entry(player, info, is_online, color))

        resp.append(self._create_pagination_controls(index, pages))
        source.reply(resp)

    def get_player(self, source: CommandSource, context: dict) -> None:
        """获取玩家信息"""
        player = context['player']
        online_players = get_online_players(self.server)

        if player in online_players:
            total_seconds = self._get_total_seconds(player)
            total_str = self._format_total_seconds(total_seconds)
            resp = RText(f'玩家{player}当前在线, 总在线时长 {total_str}').set_color(RColor.green)
        elif player in self.data:
            record = self.data[player]
            player_info = create_player_info(player, record, self.config)
            resp = (RText(f'玩家{player}最近的游玩时间为{record.last_date.strftime("%Y-%m-%d")}, 总在线时长 {player_info.formatted_total_time}')
                    .set_color(player_info.activity.color))
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
            self._session_start_times.pop(player, None)
            resp = RText(f'已清除玩家{player}最近的游玩时间').set_color(RColor.green)
        else:
            resp = RText(f'当前没有玩家{player}的游玩时间').set_color(RColor.red)

        source.reply(resp)

    def reset_player_total(self, source: CommandSource, context: dict) -> None:
        """重置玩家的累计在线时长"""
        if self.server.get_permission_level(source) < 3:
            return source.reply(RText('你没有权限重置玩家的累计在线时长').set_color(RColor.red))

        player = context['player']
        record = self.data.get(player)
        if record is None:
            return source.reply(RText(f'当前没有玩家{player}的游玩记录').set_color(RColor.red))

        record.total_seconds = 0
        if player in self._session_start_times:
            self._session_start_times[player] = datetime.now()

        save_player_data(self.server, self.data)
        source.reply(RText(f'已重置玩家{player}的累计在线时长').set_color(RColor.green))

    def mark_player_joined(self, player: str) -> None:
        """记录玩家加入时间"""
        if not self._is_trackable(player):
            self._session_start_times.pop(player, None)
            return

        self._session_start_times[player] = datetime.now()

    def update_player_time(self, player: str) -> None:
        """更新玩家最后游玩时间并累计在线时长"""
        if not self._is_trackable(player):
            self._session_start_times.pop(player, None)
            return

        now = datetime.now()
        session_start = self._session_start_times.pop(player, None)
        record = self.data.get(player)

        if record is None:
            record = PlayerRecord(last_date=now)
            self.data[player] = record

        record.last_date = now

        if session_start is not None:
            session_seconds = int((now - session_start).total_seconds())
            record.add_session(session_seconds)
        else:
            self.server.logger.debug(f'player {player} left without recorded join time, skipping session accumulation')

        save_player_data(self.server, self.data)
        self.server.logger.debug(f'player {player} last play time updated!!')

    def _prepare_player_list(self, online_players: List[str]) -> List[Tuple[str, Optional[PlayerInfo], bool, RColor]]:
        """准备玩家列表数据"""
        result_list: List[Tuple[str, Optional[PlayerInfo], bool, RColor]] = []

        # 添加在线玩家
        for player in online_players:
            if not self._is_trackable(player):
                continue
            info = create_player_info(player, self.data[player], self.config) if player in self.data else None
            result_list.append((player, info, True, RColor.green))

        # 添加离线玩家
        offline_players: List[PlayerInfo] = []
        for player, record in self.data.items():
            if player not in online_players:
                player_info = create_player_info(player, record, self.config)
                offline_players.append(player_info)

        sorted_players = sort_players(offline_players, self.config.reverse)
        for player in sorted_players:
            result_list.append((player.name, player, False, player.activity.color))

        return result_list

    def _format_player_entry(self, player: str, info: Optional[PlayerInfo], is_online: bool, color: RColor) -> RText:
        """格式化玩家条目"""
        if is_online:
            total_seconds = self._get_total_seconds(player)
            total_str = self._format_total_seconds(total_seconds)
            return RText(f'|-> {player}:在线(总时长 {total_str})\n', color=color)

        if info is None:
            return RText(f'|-> {player}:暂无数据\n', color=RColor.gray)

        days = info.days_offline
        date_str = info.record.last_date.strftime('%Y-%m-%d')
        return RText(f'|-> {player}:{date_str}({days}天未上线, 总时长 {info.formatted_total_time})\n', color=color)

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

    def _warm_up_online_sessions(self) -> None:
        """初始化当前在线玩家的会话开始时间"""
        now = datetime.now()
        for player in get_online_players(self.server):
            if self._is_trackable(player):
                self._session_start_times[player] = now

    def _is_trackable(self, player: str) -> bool:
        if is_ignore_player(player, self.config.ignorePlayerRegexes):
            return False
        if self.config.only_whitelist_player:
            whitelist_players = get_whitelist_players(self.server)
            return player in whitelist_players
        return True

    def _get_total_seconds(self, player: str) -> int:
        record = self.data.get(player)
        total = record.total_seconds if record else 0
        session_start = self._session_start_times.get(player)
        if session_start:
            total += int((datetime.now() - session_start).total_seconds())
        return total

    def _format_total_seconds(self, seconds: int) -> str:
        dummy_record = PlayerRecord(last_date=datetime.now(), total_seconds=seconds)
        dummy_info = PlayerInfo(name='', record=dummy_record, config=self.config)
        return dummy_info.formatted_total_time
