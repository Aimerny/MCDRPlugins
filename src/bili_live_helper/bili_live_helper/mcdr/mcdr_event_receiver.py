import abc

from bili_live_helper.bili.event_handler import EventReceiver
from bili_live_helper.bili.live_event import DanmuInfo
from bili_live_helper.plugin_context import PluginContext
from mcdreforged.api.all import *


class MCDRLiveEventReceiver(EventReceiver):
    def __init__(self, ctx: PluginContext):
        self.server = ctx.mcdr_server
        self.logger = ctx.mcdr_logger

    def forward_danmu(self, danmu: DanmuInfo):
        raise 'not implement!'

    @staticmethod
    def mcdr_forward_format(user: str, content: str) -> RTextBase:
        return RTextList(
            RText(text="[Bilibili-Live](", color=RColor.dark_aqua),
            RText(text=user, color=RColor.gray),
            RText(text="):", color=RColor.dark_aqua),
            RText(text=content, color=RColor.white)
        )


class PersonalEventReceiver(MCDRLiveEventReceiver):
    def __init__(self, ctx: PluginContext, owner: str):
        super().__init__(ctx)
        self.owner = owner

    def forward_danmu(self, danmu: DanmuInfo):
        self.server.tell(player=self.owner, text=self.mcdr_forward_format(danmu.user, danmu.content))


class BroadcastEventReceiver(MCDRLiveEventReceiver):
    def forward_danmu(self, danmu: DanmuInfo):
        self.server.broadcast(text=self.mcdr_forward_format(danmu.user, danmu.content))


class ConsoleEventReceiver(MCDRLiveEventReceiver):
    def forward_danmu(self, danmu: DanmuInfo):
        self.logger.info(f'[Bilibili-Live]({danmu.user}):{danmu.content}')
