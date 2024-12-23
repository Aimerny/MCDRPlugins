from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from mcdreforged.api.all import RColor

from player_last_play.config import Config


class ActivityLevel(Enum):
    ACTIVE = auto()
    NORMAL = auto()
    INACTIVE = auto()
    DANGER = auto()

    @property
    def color(self) -> RColor:
        if self == ActivityLevel.ACTIVE:
            return RColor.green
        elif self == ActivityLevel.NORMAL:
            return RColor.yellow
        elif self == ActivityLevel.INACTIVE:
            return RColor.gold
        else:
            return RColor.red


@dataclass
class PlayerInfo:
    name: str
    last_date: datetime
    config: Config

    @property
    def activity(self) -> ActivityLevel:
        days = (datetime.now() - self.last_date).days

        if days < self.config.active:
            return ActivityLevel.ACTIVE
        elif self.config.active <= days < self.config.normal:
            return ActivityLevel.NORMAL
        elif self.config.normal <= days < self.config.inactive:
            return ActivityLevel.INACTIVE
        else:
            return ActivityLevel.DANGER

    @property
    def days_offline(self) -> int:
        return (datetime.now() - self.last_date).days 