from mcdreforged.api.all import PluginServerInterface

from offline_whitelist_reforged import Config
from offline_whitelist_reforged.util import load_whitelist
from offline_whitelist_reforged.command_handler import CommandHandler


class Plugin:

    @property
    def server(self):
        return self.__server

    @property
    def whitelist(self):
        return self.__whitelist

    @property
    def command_handler(self):
        return self.__command_handler

    @property
    def config(self):
        return self.__config

    def __init__(self, server: PluginServerInterface, config: Config):
        self.__server = server
        self.__whitelist = load_whitelist(server)
        self.__command_handler = CommandHandler(server, config, self.__whitelist)
        self.__config = config
