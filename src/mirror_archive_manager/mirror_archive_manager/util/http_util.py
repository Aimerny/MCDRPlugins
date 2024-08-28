import json
from enum import Enum
from typing import Optional

from mcdreforged.api.all import *
from mirror_archive_manager.util.mcdr_util import reply_message, tr
from mirror_archive_manager.config.mirror_server_config import MirrorServerConfig
import requests


class OperateType(Enum):
    START = "start"
    STOP = "stop"
    SYNC = "sync"
    INFO = "info"

    def __str__(self):
        return self.name.lower()


def request_mirror(source: CommandSource, mirror: MirrorServerConfig, op_type: OperateType,
                   data: dict | None = None) -> Optional[any]:
    try:
        url = f'http://{mirror.host}:{mirror.port}/{op_type}'
        resp = requests.post(url=url, timeout=3, data=json.dumps(data))
        return resp.content
    except Exception as e:
        reply_message(source,
                      tr('connection_error', RText(mirror.name, RColor.dark_aqua), RText(e, RColor.dark_red)))
        return None
