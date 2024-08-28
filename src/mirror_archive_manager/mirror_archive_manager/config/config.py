import functools

from mcdreforged.api.all import Serializable
from typing import List, Optional

from mirror_archive_manager.config.mirror_server_config import MirrorServerConfig
from mirror_archive_manager.config.perm_config import PermConfig


class Config(Serializable):
    main: bool = True
    mirrors: List[MirrorServerConfig] = [MirrorServerConfig()]
    main_path: str = '../main-server'
    port: int = 30075
    perms: PermConfig = PermConfig()

    @classmethod
    @functools.lru_cache
    def __get_default(cls) -> 'Config':
        return Config.get_default()

    @classmethod
    def get(cls) -> 'Config':
        if _config is None:
            return cls.__get_default()
        return _config


_config: Optional[Config] = None


def set_config_instance(cfg: Config):
    global _config
    _config = cfg
