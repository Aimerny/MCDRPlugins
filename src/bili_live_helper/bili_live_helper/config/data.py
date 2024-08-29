from typing import Dict, Optional

from mcdreforged.api.all import *

from bili_live_helper.config.live_config import LiveConfig


class DataConfig(Serializable):
    lives: Dict[str, LiveConfig] = {}
