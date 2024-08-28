from typing import Optional, List

from mcdreforged.api.all import *

from mirror_archive_manager.config.config import Config
from mirror_archive_manager.config.mirror_server_config import MirrorServerConfig
from mirror_archive_manager.manage.main_processor import MainProcessor
from mirror_archive_manager.util.mcdr_util import reply_message, tr
from mirror_archive_manager.globals import disable

COMMAND_HELP_LIST = ['start', 'stop', 'sync', 'info']


class CommandManager:
    def __init__(self, server: PluginServerInterface, processor: MainProcessor):
        self.server = server
        self.config = Config.get()
        self.processor = processor

    def cmd_help(self, source: CommandSource, context: dict):
        what = context.get('what')
        if what is not None and what not in COMMAND_HELP_LIST:
            reply_message(source, tr('help.unknown_help', RText(f'!!mam {what}', RColor.red)))
            return
        else:
            self.help_process(source, what)

    @classmethod
    def help_process(cls, source: CommandSource, what: Optional[str]):
        reply_message(source, tr('help.help_header'))
        if what is None:
            reply_message(source, tr('help.start_help', RText(f'!!mam start <server_name>', RColor.gray)))
            reply_message(source, tr('help.stop_help', RText(f'!!mam stop <server_name>', RColor.gray)))
            reply_message(source, tr('help.sync_help', RText(f'!!mam sync <server_name> <id>', RColor.gray)))
            # reply_message(source, tr('help.info_help', RText(f'!!mam info <server_name>', RColor.gray)))
        elif what == 'start':
            reply_message(source, tr('help.start_help', RText(f'!!mam start <server_name>', RColor.gray)))
        elif what == 'stop':
            reply_message(source, tr('help.stop_help', RText(f'!!mam stop <server_name>', RColor.gray)))
        elif what == 'sync':
            reply_message(source, tr('help.sync_help', RText(f'!!mam sync <server_name> <backup_id>', RColor.gray)))
        # elif what == 'info':
        #     reply_message(source, tr('help.info_help', RText(f'!!mam info <server_name>', RColor.gray)))
        reply_message(source, tr('help.help_footer'))

    def cmd_start(self, source: CommandSource, context: dict):
        if source.get_permission_level() < self.config.perms.start:
            reply_message(source, tr('perm_denied').set_color(RColor.red))
            return
        mirror_config = self.__parse_mirror_config(source, context)
        if mirror_config is None:
            return
        self.processor.start_mirror(source, mirror_config)

    def cmd_stop(self, source: CommandSource, context: dict):
        if source.get_permission_level() < self.config.perms.stop:
            reply_message(source, tr('perm_denied').set_color(RColor.red))
            return
        mirror_config = self.__parse_mirror_config(source, context)
        if mirror_config is None:
            return
        self.processor.stop_mirror(source, mirror_config)

    def cmd_sync(self, source: CommandSource, context: dict):
        if source.get_permission_level() < self.config.perms.sync:
            reply_message(source, tr('perm_denied').set_color(RColor.red))
            return
        mirror_config = self.__parse_mirror_config(source, context)
        if mirror_config is None:
            return
        backup_id = context.get('backup_id')
        if backup_id is None:
            reply_message(source, tr('no_backup_id_found').set_color(RColor.dark_red))
        self.processor.sync_mirror(source, backup_id, mirror_config)

    def cmd_info(self, source: CommandSource, context: dict):
        pass

    def __suggest_mirror_server(self) -> List[str]:
        mirrors = self.config.mirrors
        if mirrors is not None:
            return [mirror.name for mirror in mirrors]
        else:
            return []

    def __parse_mirror_config(self, source: CommandSource, context: dict) -> MirrorServerConfig | None:
        mirror_name = context.get('server')
        if len(self.config.mirrors) == 0:
            reply_message(source, tr('no_mirror_found').set_color(RColor.dark_red))
            return None
        mirror_config_map = {conf.name: conf for conf in self.config.mirrors}
        if mirror_name is None:
            mirror_config = self.config.mirrors[0]
        else:
            mirror_config = mirror_config_map.get(mirror_name)
            if mirror_config is None:
                reply_message(source, tr('no_mirror_found').set_color(RColor.dark_red))
                return None
        return mirror_config

    def register_commands(self):
        builder = SimpleCommandBuilder()
        # help command
        builder.command('help', self.cmd_help)
        builder.command('help <what>', self.cmd_help)
        builder.arg('what', Text).suggests(lambda: COMMAND_HELP_LIST)
        # start command
        builder.command('start', self.cmd_start)
        builder.command('start <server>', self.cmd_start)
        # stop command
        builder.command('stop', self.cmd_stop)
        builder.command('stop <server>', self.cmd_stop)
        # sync command
        builder.command('sync <backup_id>', self.cmd_sync)
        builder.command('sync <backup_id> <server>', self.cmd_sync)
        # info command
        # builder.command('info', self.cmd_info)
        # builder.command('info <server>', self.cmd_info)

        builder.arg('server', Text).suggests(lambda: self.__suggest_mirror_server())
        builder.arg('backup_id', Integer)

        root = (
            Literal('!!mam').
            requires(lambda: not disable, lambda: RText('mam has been disabled').set_color(RColor.red))
            .runs(self.cmd_help)
        )
        builder.add_children_for(root)

        self.server.register_command(root)
