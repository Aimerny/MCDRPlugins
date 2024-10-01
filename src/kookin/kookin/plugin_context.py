from typing import Optional

from mcdreforged.api.all import *

from kookin import Config, Data, KookApi


class PluginContext:

    def __init__(self, server: PluginServerInterface,kook_api: KookApi, config: Config, data: Data):
        self.__mcdr_server = server
        self.__meta_info = server.get_self_metadata()
        self.__mcdr_logger = server.logger
        self.__mcdr_config = config
        self.__mcdr_data = data
        self.__kook_api = kook_api

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

    @property
    def kook_api(self):
        return self.__kook_api

    @mcdr_config.setter
    def mcdr_config(self, config: Config):
        self.__mcdr_config = config

    @mcdr_data.setter
    def mcdr_data(self, data: Data):
        self.__mcdr_data = data

    @classmethod
    def get(cls) -> 'PluginContext':
        return _plugin_context


_plugin_context: Optional[PluginContext] = None


def load_plugin_context(ctx: PluginContext):
    global _plugin_context
    _plugin_context = ctx
