from mcdreforged.api.all import *


class LiveConfig(Serializable):
    enable: bool = True
    title: str = ''
    room_id: int = ''

