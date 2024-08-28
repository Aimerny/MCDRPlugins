from mcdreforged.api.all import *

from typing import Optional
from mirror_archive_manager.config.config import Config, set_config_instance
from mirror_archive_manager import globals
from mirror_archive_manager.command.mam_command import CommandManager
from mirror_archive_manager.manage.main_processor import MainProcessor
from mirror_archive_manager.manage.mirror_processor import MirrorProcessor
from mirror_archive_manager.manage.processor import Processor

config: Optional[Config] = None
_has_loaded = False
processor: Processor

globals.load()


def is_main() -> bool:
    return config.main


def on_load(server: PluginServerInterface, old):
    global config, _has_loaded
    try:
        config = server.load_config_simple(target_class=Config, failure_policy='raise')
        set_config_instance(config)
        if is_main():
            server.logger.info(f'MAM running with main role!')
            start_main(server)
        else:
            server.logger.info(f'MAM running with mirror role!')
            start_mirror(server)

    except Exception:
        server.logger.error(f'{server.get_self_metadata().name} initialization failed!')
        on_unload(server)
        raise
    else:
        _has_loaded = True
        server.logger.info(f'{server.get_self_metadata().name} initialization completed!')
        return


def on_unload(server: PluginServerInterface):
    processor.stop()
    server.logger.warning(f'{server.get_self_metadata().name} unloaded!')


def start_main(server: PluginServerInterface):
    global processor
    if len(config.mirrors) == 0:
        server.logger.warning('mirror server not found! MAM has been disabled!')
        globals.disable = True
    # register commands
    processor = MainProcessor(server, config)
    command_manager = CommandManager(server, processor)
    command_manager.register_commands()


def start_mirror(server: PluginServerInterface):
    global processor
    processor = MirrorProcessor(server, config)
    processor.start()
    server.logger.info('mirror process...')
