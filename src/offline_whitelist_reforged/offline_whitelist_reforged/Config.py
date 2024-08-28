from mcdreforged.api.all import *


class PermConfig(Serializable):
    on: int = 4
    off: int = 4
    list: int = 2
    add: int = 3
    remove: int = 3


class Config(Serializable):
    perms: PermConfig = PermConfig()
