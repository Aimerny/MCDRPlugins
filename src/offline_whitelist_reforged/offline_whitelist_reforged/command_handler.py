from mcdreforged.api.all import *

from offline_whitelist_reforged import Config
from offline_whitelist_reforged.util import replace_code
from whitelist_api import WhitelistException

help_msg = '''-------- §a Offline Whitelist Reforged §r--------
§b!!wr help §f- §c显示帮助消息
§b!!wr list §f- §c显示全部玩家的白名单
§b!!wr add <player> §f- §c 为<player>添加白名单
§b!!wr remove <player> §f- §c 移除<player>的白名单
§b!!wr on §f- §c打开白名单
§b!!wr off §f- §c关闭白名单
---------------------------------------------
'''


def help_info(server):
    for line in help_msg.splitlines():
        server.reply(line)


class CommandHandler:

    def __init__(self, server: PluginServerInterface, config: Config):
        self.server = server
        self.__whitelist_api = server.get_plugin_instance('whitelist_api')
        self.register_commands()
        self.config = config

    def register_commands(self):
        server = self.server
        server.register_help_message('!!wr', '离线服务器白名单管理插件')
        command_builder = SimpleCommandBuilder()

        command_builder.command('!!wr', help_info)
        command_builder.command('!!wr help', help_info)
        command_builder.command('!!wr on', self.enable_whitelist)
        command_builder.command('!!wr off', self.disable_whitelist)
        command_builder.command('!!wr list', self.get_list)
        command_builder.command('!!wr add <player>', self.add_player)
        command_builder.command('!!wr remove <rm_player>', self.remove_player)
        command_builder.arg('player', Text)
        command_builder.arg('rm_player', Text).suggests(self.__whitelist_api.get_whitelist_names)
        command_builder.register(server)

    def get_list(self, server):

        if self.server.get_permission_level(server) < self.config.perms.list:
            resp = f'&c你没有权限查看白名单，请确保权限等级不低于{PermissionLevel.from_value(self.config.perms.list)}'
        else:
            resp = '---- &a白名单 &r----\n'
            sorted_list = sorted(self.__whitelist_api.get_whitelist(), key=lambda p: p.name)
            index = 1
            for player in sorted_list:
                resp = resp + f'{index}. {player.name}\n'
                index += 1
            resp = resp + f'---- &a共{len(sorted_list)}人 &r----'
        server.reply(replace_code(resp))

    def add_player(self, source, context):
        if self.server.get_permission_level(source) < self.config.perms.add:
            source.reply(replace_code(
                f'&c你没有权限添加白名单，请确保权限等级不低于{PermissionLevel.from_value(self.config.perms.add)}'))
        else:
            player = context['player']
            try:
                self.__whitelist_api.add_offline_player(player)
                source.reply(replace_code(f'&a玩家{player}已添加至白名单'))
            except WhitelistException:
                source.reply(replace_code(f'&e玩家{player}已经在白名单中了'))

    def remove_player(self, source: CommandSource, context: CommandContext):
        if self.server.get_permission_level(source) < self.config.perms.remove:
            source.reply(replace_code(
                f'&c你没有权限移除白名单，请确保权限等级不低于{PermissionLevel.from_value(self.config.perms.remove)}'))
        else:
            player = context.get('rm_player')
            try:
                self.__whitelist_api.remove_player(player)
                source.reply(replace_code(f'&a已经移除{player}的白名单'))
            except WhitelistException:
                source.reply(replace_code(f'&e玩家{player}不在白名单中'))

    def enable_whitelist(self, server):
        if self.server.get_permission_level(server) < self.config.perms.on:
            resp = f'&c你没有权限打开白名单，请确保权限等级不低于{PermissionLevel.from_value(self.config.perms.on)}'
        else:
            self.__whitelist_api.enable_whitelist()
            resp = f'&a白名单已打开'
        server.reply(replace_code(resp))

    def disable_whitelist(self, server):
        if self.server.get_permission_level(server) < self.config.perms.off:
            resp = f'&c你没有权限关闭白名单，请确保权限等级不低于{PermissionLevel.from_value(self.config.perms.off)}'
        else:
            self.__whitelist_api.disable_whitelist()
            resp = f'&e白名单已关闭'
        server.reply(replace_code(resp))
