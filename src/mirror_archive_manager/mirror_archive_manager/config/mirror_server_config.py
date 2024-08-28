from typing import Optional

from mcdreforged.api.all import Serializable


class MirrorServerConfig(Serializable):
    name: Optional[str] = 'mirror'
    pb_archive_id: int = 0
    host: str = '127.0.0.1'
    port: int = 30076
