from typing import Type, Optional

from mcdreforged.api.all import *


class AccountConfig(Serializable):
    uid: int = 0
    sessdata: str = ''
    bili_jct: str = ''
    buvid3: str = ''
    ac_time_value: str = ''


class Config(Serializable):
    enable: bool = True
    data_file_path: str = 'data.json'
    account: AccountConfig = AccountConfig()