from mcdreforged.api.all import *

from bili_live_helper.plugin_context import PluginContext


class CommandManager:
    def __init__(self, ctx: PluginContext):
        self.server = ctx.mcdr_server
        self.logger = self.server.logger

    def cmd_help(self, context: CommandContext):
        pass

    def cmd_bind_room(self, context: CommandContext):
        pass

    def cmd_enable(self, context: CommandContext):
        pass

    def cmd_live_info(self, context: CommandContext):
        pass

    def cmd_player_live_info(self, contest: CommandContext):
        pass

    def register_command(self):
        builder = SimpleCommandBuilder()
        builder.command("!!blh", self.cmd_help)
        builder.command("!!blh help", self.cmd_help)
        builder.command("!!blh bind <rid>", self.cmd_bind_room)
        builder.command("!!blh enable", self.cmd_enable)
        builder.command("!!blh info", self.cmd_live_info)
        builder.command("!!blh info <player>", self.cmd_player_live_info)
        builder.arg("rid", Text)
        builder.arg("player", Text)

        builder.register(server=self.server)
