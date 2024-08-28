import threading
import time
from pathlib import Path

from mirror_archive_manager.config.config import Config
from mcdreforged.api.all import *
from fastapi import FastAPI
import uvicorn

from mirror_archive_manager.manage.processor import Processor
from mirror_archive_manager.util.http_util import OperateType
from prime_backup.action.list_backup_action import ListBackupAction
from prime_backup.mcdr.command.commands import CommandManager
from prime_backup.mcdr.task.backup.import_backup_task import ImportBackupTask
from prime_backup.mcdr.task.backup.restore_backup_task import RestoreBackupTask
from prime_backup.mcdr.task_manager import TaskManager
from prime_backup.types.standalone_backup_format import StandaloneBackupFormat


class MirrorHttpServer:

    def __init__(self, api: FastAPI, config: Config):
        self.api = api
        self.server = None
        self.config = config
        self.server_thread = None

    def start(self):
        def __start_server():
            server_config = uvicorn.Config(app=self.api, host='0.0.0.0', port=self.config.port, log_level='info')
            self.server = uvicorn.Server(server_config)
            self.server.run()

        self.server_thread = threading.Thread(name='mirror-http-server', target=__start_server)
        self.server_thread.start()

    def stop(self):
        self.server.should_exit = True
        self.server_thread.join()


class MirrorProcessor(Processor):
    config: Config
    server: PluginServerInterface
    __http_server: MirrorHttpServer

    def __init__(self, server: PluginServerInterface, config: Config):
        self.api = FastAPI()
        self.server = server
        self.config = config
        self.add_routes()
        self.pb_command_manager: CommandManager = server.get_plugin_instance('prime_backup').command_manager
        self.task_manager: TaskManager = server.get_plugin_instance('prime_backup').task_manager

    def add_routes(self):
        @self.api.post(f'/{OperateType.START.value}')
        async def start_mirror():
            self.server.logger.info('start mirror')
            if self.server.is_server_running():
                return 'skip'
            else:
                self.server.start()
            return 'ok'

        @self.api.post(f'/{OperateType.STOP.value}')
        async def stop_mirror():
            self.server.logger.info('stop mirror')
            if self.server.is_server_running():
                self.server.stop()
                return 'ok'
            else:
                return 'server has been down'

        @self.api.post(f'/{OperateType.SYNC.value}')
        async def sync_archive(path_config: dict):
            self.server.logger.warning('start sync archive to this server')
            path = path_config.get('path')
            main_server_conf = self.config.main_path
            full_path = main_server_conf + '/' + path

            @new_thread
            def submit_pb_back(_, err):
                time.sleep(1)
                if err is None:
                    backup_ids = sorted([backup.id for backup in ListBackupAction().run()], reverse=True)
                    latest_backup = backup_ids[0]
                    self.task_manager.add_task(RestoreBackupTask(
                        self.server.get_plugin_command_source(),
                        latest_backup,
                        needs_confirm=False,
                        fail_soft=False,
                        verify_blob=True))

            self.task_manager.add_task(ImportBackupTask(
                source=self.server.get_plugin_command_source(),
                file_path=Path(full_path),
                backup_format=StandaloneBackupFormat.tar,
                ensure_meta=True,
                meta_override=None
            ), callback=submit_pb_back)

    def start(self):
        self.__init_http_server()

    def __init_http_server(self):
        self.__http_server = MirrorHttpServer(self.api, self.config)
        self.__http_server.start()
        self.server.logger.info(f'mirror http server started...')

    def stop(self):
        self.server.logger.info('mirror http server shutdown...')
        self.__http_server.stop()
