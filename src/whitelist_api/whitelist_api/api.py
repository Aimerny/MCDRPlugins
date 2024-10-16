import json
import logging
from json import JSONDecodeError
from typing import List

watch_enable: False

try:
    from watchdog.observers import Observer
    from watchdog.events import *

    logging.basicConfig(level=logging.INFO)
    logging.info('import "watchdog" success')
    watch_enable = True
except ImportError as err:
    logging.warning(
        'dynamic whitelist depends "watchdog" module, use "pip install watchdog" to install it if you need.')


class PlayerInfo:
    name: str
    uuid: str

    def __init__(self, name, uuid):
        self.name = name
        self.uuid = uuid


class FileEventHandler(FileSystemEventHandler):
    def __init__(self, whitelist_api: 'WhitelistApi'):
        super().__init__()
        self.__api = whitelist_api

    def on_modified(self, event: DirModifiedEvent | FileModifiedEvent) -> None:
        # compare relative path with absolute path
        if event.src_path.endswith(self.__api.whitelist_file_path()):
            self.__api.load_whitelist()


class WhitelistApi:
    __server_path: str
    __whitelist: List[PlayerInfo]
    __watchdog: Observer
    __logger: logging.Logger
    __running: bool
    __online_mode: bool

    @property
    def server_directory(self):
        return self.__server_path

    @property
    def whitelist(self):
        return self.__whitelist

    @property
    def online_mode(self):
        return self.__online_mode

    def whitelist_file_path(self):
        return f'{self.__server_path}/whitelist.json'

    def __init__(self, file_path: str, logger: logging.Logger = logging.getLogger("whitelist_api")):
        self.__server_path = file_path
        self.__logger = logger
        self.load_whitelist()
        self.__running = False
        self.refresh_online_mode()
        if watch_enable:
            self.start_watchdog()

    def load_whitelist(self):
        self.__logger.warning('whitelist loading action was triggered')
        whitelist = []
        with open(self.whitelist_file_path(), 'r', encoding='UTF-8') as f:
            try:
                whitelist_json = json.load(f)
            except JSONDecodeError as err:
                self.__logger.error(f'whitelist file is invalid: {err.msg}')
                return
        for player in whitelist_json:
            whitelist.append(PlayerInfo(player['name'], player['uuid']))
        self.__whitelist = whitelist
        # self.__logger.info(self.__whitelist)

    def save_whitelist(self):
        whitelist_json = []
        for player_info in self.__whitelist:
            whitelist_json.append({'uuid': player_info.uuid, 'name': player_info.name})
        with open(self.whitelist_file_path(), 'w', encoding='UTF-8') as f:
            f.write(json.dumps(whitelist_json, indent=2, separators=(',', ':'), ensure_ascii=False))

    def remove_player(self, player: str) -> bool:
        for index, p in enumerate(self.__whitelist):
            if p.name == player:
                self.__whitelist.remove(p)
                self.save_whitelist()
                return True
        return False

    def start_watchdog(self):
        if self.__running:
            return
        handler = FileEventHandler(self)
        self.__watchdog = Observer()
        self.__watchdog.schedule(handler, path=self.__server_path, recursive=False)
        self.__watchdog.start()
        self.__running = True

    def stop_watchdog(self):
        if self.__running:
            self.__watchdog.stop()
        self.__logger.info('whitelist api watchdog stopped')

    def refresh_online_mode(self) -> bool | None:
        with open(f'{self.server_directory}/server.properties', mode='r', encoding='UTF-8') as props:
            line = props.readline()
            while line:
                # skip '\n'
                kv = line[:-1].split('=')
                if len(kv) == 2 and kv[0] == 'online-mode':
                    self.__online_mode = True if kv[1] == 'true' else False
                    return self.__online_mode
                line = props.readline()
        return None
