import time

from mirror_archive_manager.config.config import Config
from mirror_archive_manager.config.mirror_server_config import MirrorServerConfig
from mirror_archive_manager.task.transfer_archive_task import TransferArchiveTask
from mirror_archive_manager.util.http_util import OperateType, request_mirror
from mirror_archive_manager.util.mcdr_util import reply_message, tr, deco_message
from mirror_archive_manager.manage.processor import Processor
from mcdreforged.api.all import *

from prime_backup.mcdr.command.commands import CommandManager
from prime_backup.mcdr.task_manager import TaskManager

from prime_backup.mcdr.task.backup.export_backup_task import ExportBackupTask
from prime_backup.types.standalone_backup_format import StandaloneBackupFormat


class MainProcessor(Processor):
    pb_api: CommandManager
    default_export_format: StandaloneBackupFormat = StandaloneBackupFormat.tar

    def __init__(self, server: PluginServerInterface, config: Config):
        self.server = server
        self.config = config
        self.__logger = server.logger
        self.pb_command_manager: CommandManager = server.get_plugin_instance('prime_backup').command_manager
        self.task_manager: TaskManager = server.get_plugin_instance('prime_backup').task_manager

    def start(self):
        pass

    def stop(self):
        pass

    def start_mirror(self, source: CommandSource, *args):
        mirror = args[0]
        self.__logger.debug(f'starting mirror: {mirror.name}')
        resp = request_mirror(source, mirror, OperateType.START)
        if resp is None:
            self.server.broadcast(deco_message(
                tr('start.start_failed', RText(mirror.name, RColor.dark_aqua)).set_color(RColor.dark_red)))
        else:
            self.server.broadcast(deco_message(
                tr('start.start_success', RText(mirror.name, RColor.dark_aqua).set_color(RColor.green)))
            )

    def stop_mirror(self, source: CommandSource, *args):
        mirror = args[0]
        self.__logger.debug(f'stopping mirror: {mirror.name}')
        resp = request_mirror(source, mirror, OperateType.STOP)
        if resp is None:
            self.server.broadcast(deco_message(
                tr('stop.stop_failed', RText(mirror.name, RColor.dark_aqua)).set_color(RColor.dark_red)))
        else:
            self.server.broadcast(deco_message(
                tr('stop.stop_success', RText(mirror.name, RColor.dark_aqua).set_color(RColor.green)))
            )

    def get_mirror_info(self, source: CommandSource):
        pass

    def sync_mirror(self, source: CommandSource, *args):
        backup_id: int = args[0]
        mirror: MirrorServerConfig = args[1]
        self.transfer_archive(source, backup_id, mirror)
        return

    def transfer_archive(self, source: CommandSource, backup_id: int, mirror_config: MirrorServerConfig):
        @new_thread('submit-transfer-task')
        def submit_transfer_task(_, err):
            # wait callback finish
            time.sleep(1)
            if err is None:
                self.task_manager.add_task(
                    TransferArchiveTask(source=source, backup_id=backup_id, mirror_config=mirror_config,
                                        export_format=self.default_export_format))

        self.task_manager.add_task(ExportBackupTask(
            source, backup_id, export_format=self.default_export_format,
            fail_soft=False, overwrite_existing=False, verify_blob=False, create_meta=True),
            callback=submit_transfer_task)

