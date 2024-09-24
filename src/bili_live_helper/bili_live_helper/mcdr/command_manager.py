from typing import Union

from mcdreforged.api.all import *

from bili_live_helper.config.live_config import LiveConfig
from bili_live_helper.mcdr.bili_manager import BiliManager, OptionEnum
from bili_live_helper.plugin_context import PluginContext
from bili_live_helper.util.conf_util import save_data
from bili_live_helper.util.tr_util import tr, reply_message, reply_error_message, reply_info_message, reply_warn_message


class CommandManager:
    def __init__(self, ctx: PluginContext, bili_manager: BiliManager):
        self.plg_ctx = ctx
        self.bili_manager = bili_manager

    @staticmethod
    def cmd_help(source: CommandSource, context: CommandContext):
        prefix = RText(">> !!blh")
        separator = RText(' - | - ', RColor.dark_gray)
        help_message = RTextList(
            tr('help.header').set_color(RColor.dark_aqua), '\n',
            RTextList(prefix, ' [help]', separator, tr('help.help_desc').set_color(RColor.yellow)).c(
                RAction.run_command, '!!blh help'),
            '\n',
            RTextList(prefix, ' bind ', RText('<rid>').set_color(RColor.gray).h('直播间id'), separator,
                      tr('help.bind_desc').set_color(RColor.yellow)).c(
                RAction.suggest_command, '!!blh bind '), '\n',
            RTextList(prefix, ' on', separator, tr('help.on_desc').set_color(RColor.yellow)).c(RAction.run_command,
                                                                                               '!!blh on'), '\n',
            RTextList(prefix, ' off', separator, tr('help.off_desc').set_color(RColor.yellow)).c(RAction.run_command,
                                                                                                 '!!blh off'), '\n',
            RTextList(prefix, ' info', separator, tr('help.info_desc').set_color(RColor.yellow)).c(RAction.run_command,
                                                                                                   '!!blh info'), '\n',
            RTextList(prefix, ' query', separator,
                      tr('help.query_desc').set_color(RColor.yellow)).c(RAction.suggest_command, '!!blh query '), '\n',
            RTextList(prefix, ' send ', RText('<danmu>').set_color(RColor.gray).h('弹幕内容'), separator,
                      tr('help.send_desc').set_color(RColor.yellow)).c(RAction.suggest_command, '!!blh send '), '\n',
            RTextList(prefix, ' s ', RText('<danmu>').set_color(RColor.gray).h('弹幕内容'), separator,
                      tr('help.send_desc').set_color(RColor.yellow)).c(RAction.suggest_command, '!!blh s '), '\n',

            tr('help.footer').set_color(RColor.dark_aqua)

        )
        reply_message(source, help_message, with_prefix=False)

    def cmd_bind_room(self, source: CommandSource, context: CommandContext):
        if source.is_console:
            return reply_message(source, tr('raise_message.player_command'))
        if isinstance(source, PlayerCommandSource):
            if self.bili_manager.query_player_live_status(source.player):
                return reply_error_message(source, tr('raise_message.not_allow_rebind_listener_running',
                                                      RText(source.player, RColor.gray)))
            room_id = context.get('rid')
            if room_id is None:
                return reply_error_message(source, tr('bind.room_id_invalid'))
            lives = self.plg_ctx.mcdr_data.lives
            if lives.get(source.player) is None:
                new_live_conf = LiveConfig()
                new_live_conf.enable = True
                new_live_conf.room_id = room_id
                lives[source.player] = new_live_conf
                reply_info_message(source, tr('bind.create_room_id', RText(room_id, RColor.red),
                                              RText(room_id, RColor.dark_green)))
            else:
                live_conf = lives.get(source.player)
                old_rood_id = lives.get(source.player).room_id
                live_conf.room_id = room_id
                # reply update room id message to source
                reply_info_message(source, tr('bind.update_room_id', RText(old_rood_id, RColor.red),
                                              RText(room_id, RColor.dark_green)))
        # save bound live config
        save_data()

    def cmd_on(self, source: CommandSource, context: CommandContext):
        if source.is_console:
            return reply_message(source, tr('raise_message.player_command'))
        if isinstance(source, PlayerCommandSource):
            player = source.player
            lives_conf = self.plg_ctx.mcdr_data.lives
            live_conf = lives_conf.get(player)
            if live_conf is None:
                return reply_error_message(source, tr('raise_message.live_conf_notfound', RText(player, RColor.yellow)))
            if self.bili_manager.is_listener_running(player):
                return reply_warn_message(source, tr('raise_message.listener_is_running',
                                                     RText(live_conf.room_id, RColor.yellow)))
            self.bili_manager.submit(player, OptionEnum.RUN)
            return reply_info_message(source, tr('reply_message.run_listener', RText(live_conf.room_id, RColor.white)))

    def cmd_off(self, source: CommandSource, context: CommandContext):
        if source.is_console:
            return reply_message(source, tr('raise_message.player_command'))
        if isinstance(source, PlayerCommandSource):
            player = source.player
            if self.bili_manager.is_listener_running(player):
                self.bili_manager.submit(player, OptionEnum.KILL)
                return reply_info_message(source, tr('reply_message.kill_listener', RText(player, RColor.gray)))
            else:
                return reply_warn_message(source, tr('raise_message.listener_not_found', RText(player, RColor.gray)))

    def cmd_live_info(self, source: CommandSource, context: CommandContext):
        if source.is_console:
            return reply_message(source, tr('raise_message.player_command'))
        if isinstance(source, PlayerCommandSource):
            player = source.player
            lives_conf = self.plg_ctx.mcdr_data.lives
            live_conf = lives_conf.get(player)
            if live_conf is not None:
                status = self.bili_manager.query_player_live_status(player)
                return reply_message(source, self.__live_info_format(player, live_conf, status), with_prefix=False)

    def cmd_player_live_info(self, source: CommandSource, context: CommandContext):
        target = context.get('player')
        if target is None or target == '':
            return reply_error_message(source, tr('raise_message.player_missing'))
        lives_conf = self.plg_ctx.mcdr_data.lives
        live_conf = lives_conf.get(target)
        if live_conf is not None:
            status = self.bili_manager.query_player_live_status(target)
            return reply_message(source, self.__live_info_format(target, live_conf, status), with_prefix=False)

    def cmd_send_msg(self, source: CommandSource, context: CommandContext):
        if source.is_console:
            return reply_error_message(source, tr('raise_message.player_command'))
        if isinstance(source, PlayerCommandSource):
            player = source.player
            if not self.plg_ctx.mcdr_config.send:
                return reply_error_message(source, tr('raise_message.listener_send_disable'))
            status = self.bili_manager.query_player_live_status(player)
            if not status:
                return reply_error_message(source, tr('raise_message.listener_closed'))
            message = f"<{player}> {context.get('send_msg')}"
            self.bili_manager.submit(player, OptionEnum.SEND_MSG, message)

    def cmd_admin(self, source: CommandSource, context: CommandContext):
        pass

    def register_command(self):
        builder = SimpleCommandBuilder()
        builder.command("!!blh", self.cmd_help)
        builder.command("!!blh help", self.cmd_help)
        builder.command("!!blh bind <rid>", self.cmd_bind_room)
        builder.command("!!blh on", self.cmd_on)
        builder.command("!!blh off", self.cmd_off)
        builder.command("!!blh info", self.cmd_live_info)
        builder.command("!!blh query <player>", self.cmd_player_live_info)
        builder.command("!!blh s <send_msg>", self.cmd_send_msg)
        builder.command("!!blh send <send_msg>", self.cmd_send_msg)
        # builder.command("!!blh admin <type> <option>", self.cmd_admin)

        builder.arg("rid", Number)
        builder.arg("player", Text)
        builder.arg("send_msg", GreedyText)
        # builder.arg("type", Text)
        # builder.arg("option", Text)
        builder.register(server=self.plg_ctx.mcdr_server)

    @staticmethod
    def __live_info_format(player: str, live_conf: LiveConfig, status: bool) -> RTextBase:
        return RTextList(
            tr('info.header', RText(player, RColor.gray)).set_color(RColor.dark_aqua), '\n',
            tr('info.room_status_template',
               RText(tr('info.live_open') if status else RText(tr('info.live_close')), RColor.yellow)), '\n',
            tr('info.room_id_template', RText(live_conf.room_id, RColor.yellow)), '\n',
            tr('info.footer').set_color(RColor.dark_aqua)
        )
