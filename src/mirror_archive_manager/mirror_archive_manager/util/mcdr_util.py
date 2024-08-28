from mcdreforged.api.all import *
from typing import Union


def reply_message(source: CommandSource, msg: Union[str, RTextBase], *, with_prefix: bool = True):
    if with_prefix:
        msg = deco_message(msg)
    source.reply(msg)


def deco_message(msg: Union[str, RTextBase]) -> RTextBase:
    return RTextList(RTextList(RText('[MAM]', RColor.dark_aqua).h('Mirror Archive Manager'), ' '), msg)


def tr(key: str, *args, **kwargs) -> RTextBase:
    from mirror_archive_manager import globals
    return ServerInterface.si().rtr(globals.metadata.id + '.' + key, *args, **kwargs)
