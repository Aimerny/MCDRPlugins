from mcdreforged.api.all import *

from bili_live_helper.mcdr.bili_manager import BiliManager
from bili_live_helper.plugin_context import PluginContext


class CommandManager:
    def __init__(self, ctx: PluginContext, bili_manager: BiliManager):
        self.server = ctx.mcdr_server
        self.logger = self.server.logger
        self.bili_manager = bili_manager

    def cmd_help(self, source: CommandSource, context: CommandContext):
        pass

    def cmd_bind_room(self, source: CommandSource, context: CommandContext):
        pass

    def cmd_on(self, source: CommandSource, context: CommandContext):
        pass

    def cmd_off(self, source: CommandSource, context: CommandContext):
        pass

    def cmd_live_info(self, source: CommandSource, context: CommandContext):
        pass

    def cmd_player_live_info(self, source: CommandSource, context: CommandContext):
        self.bili_manager.submit(context.get('player', 'Aimerny'), 'run')

    def register_command(self):
        builder = SimpleCommandBuilder()
        builder.command("!!blh", self.cmd_help)
        builder.command("!!blh help", self.cmd_help)
        builder.command("!!blh bind <rid>", self.cmd_bind_room)
        builder.command("!!blh on", self.cmd_on)
        builder.command("!!blh off", self.cmd_off)
        builder.command("!!blh info", self.cmd_live_info)
        builder.command("!!blh info <player>", self.cmd_player_live_info)
        builder.arg("rid", Text)
        builder.arg("player", Text)

        builder.register(server=self.server)
