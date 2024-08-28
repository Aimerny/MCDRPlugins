from mcdreforged.api.all import *

from prime_backup.types.standalone_backup_format import StandaloneBackupFormat
from prime_backup.mcdr.task.basic_task import HeavyTask
from mirror_archive_manager.config.mirror_server_config import MirrorServerConfig
from mirror_archive_manager.util.mcdr_util import deco_message, tr
from mirror_archive_manager.util.http_util import request_mirror, OperateType


def _sanitize_file_name(s: str, max_length: int = 64):
    bad_chars = set(r'\/<>|:"*?' + '\0')
    s = s.strip().replace(' ', '_')
    s = ''.join(c for c in s if c not in bad_chars and ord(c) > 31)
    return s[:max_length]


class TransferArchiveTask(HeavyTask[None]):
    def __init__(self, source: CommandSource, backup_id: int, mirror_config: MirrorServerConfig,
                 export_format: StandaloneBackupFormat):
        super().__init__(source)
        self.backup_id = backup_id
        self.mirror_config = mirror_config
        self.export_format = export_format

    @property
    def id(self) -> str:
        return 'transfer_archive'

    def run(self) -> None:
        from prime_backup.action.get_backup_action import GetBackupAction
        from prime_backup.mcdr.text_components import TextComponents

        backup = GetBackupAction(self.backup_id).run()
        name = f'backup_{backup.id}'
        if len(backup.comment) > 0:
            comment = TextComponents.backup_comment(backup.comment).to_plain_text()  # use MCDR's language
            name += '_' + _sanitize_file_name(comment)
        name += f'.{self.export_format.name}'
        full_path = self.config.storage_path / 'export' / name

        payload = {
            'file_name': name,
            'path': str(full_path)
        }
        print(full_path)
        resp = request_mirror(source=self.source, mirror=self.mirror_config, op_type=OperateType.SYNC, data=payload)
        if resp is None:
            self.server.broadcast(deco_message(
                tr('sync.sync_failed',
                   self.backup_id, RText(self.mirror_config.name, RColor.dark_aqua)).set_color(RColor.dark_red)))
        else:
            self.server.broadcast(deco_message(
                tr('sync.sync_success',
                   self.backup_id, RText(self.mirror_config.name, RColor.dark_aqua).set_color(RColor.green))))
