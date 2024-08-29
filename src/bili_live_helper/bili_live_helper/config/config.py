from typing import Type, Optional

from mcdreforged.api.all import *


class Config(Serializable):
    enable: bool = True
    data_file_path: str = 'data.json'


