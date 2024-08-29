from typing import Optional

from mcdreforged.api.all import *

from bili_live_helper.config.config import Config
from bili_live_helper.config.data import DataConfig


class PluginContext:
    mcdr_server: PluginServerInterface
    mcdr_logger: MCDReforgedLogger
    mcdr_config: Config
    mcdr_data: DataConfig

    def __init__(self, server: PluginServerInterface, config: Config, data: DataConfig):
        self.__mcdr_server = server
        self.__meta_info = server.get_self_metadata()
        self.__mcdr_logger = server.logger
        self.__mcdr_config = config
        self.__mcdr_data = data

    @property
    def mcdr_server(self):
        return self.__mcdr_server

    @property
    def mcdr_logger(self):
        return self.__mcdr_logger

    @property
    def meta_info(self):
        return self.__meta_info

    @property
    def mcdr_config(self):
        return self.__mcdr_config

    @property
    def mcdr_data(self):
        return self.__mcdr_data

    @mcdr_config.setter
    def mcdr_config(self, config: Config):
        self.__mcdr_config = config

    @mcdr_data.setter
    def mcdr_data(self, data: DataConfig):
        self.__mcdr_data = data

    @classmethod
    def get(cls) -> 'PluginContext':
        return _plugin_context


_plugin_context: Optional[PluginContext] = None


def load_plugin_context(ctx: PluginContext):
    global _plugin_context
    _plugin_context = ctx

