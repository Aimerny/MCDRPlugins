from typing import Union

from mcdreforged.api.all import *


def reply_message(source: CommandSource, msg: Union[str, RTextBase], *, with_prefix: bool = True):
    if with_prefix:
        msg = deco_message(msg)
    source.reply(msg)


def reply_error_message(source: CommandSource, msg: Union[str, RTextBase]):
    source.reply(RTextList(msg).set_color(RColor.dark_red))


def reply_info_message(source: CommandSource, msg: Union[str, RTextBase]):
    source.reply(RTextList(msg).set_color(RColor.dark_aqua))


def reply_warn_message(source: CommandSource, msg: Union[str, RTextBase]):
    source.reply(RTextList(msg).set_color(RColorRGB(0xffa500)))


def deco_message(msg: Union[str, RTextBase]) -> RTextBase:
    return RTextList(RTextList(RText('[BLH]', RColor.dark_aqua).h('Bili Live Helper'), ' '), msg)


def tr(key: str, *args, **kwargs) -> RTextBase:
    from bili_live_helper.plugin_context import plugin_id
    return ServerInterface.si().rtr(plugin_id + '.' + key, *args, **kwargs)
