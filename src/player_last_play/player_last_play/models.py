from dataclasses import dataclass
from datetime import datetime
from enum import Enum, auto

from mcdreforged.api.all import RColor

from player_last_play.config import Config


@dataclass
class PlayerRecord:
    last_date: datetime
    total_seconds: int = 0

    def add_session(self, session_seconds: int) -> None:
        """Accumulate a session into the total tracked duration."""
        if session_seconds > 0:
            self.total_seconds += session_seconds


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
    record: PlayerRecord
    config: Config

    @property
    def activity(self) -> ActivityLevel:
        days = self.days_offline

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
        return (datetime.now() - self.record.last_date).days

    @property
    def formatted_total_time(self) -> str:
        """Return a compact representation of total tracked play time."""
        seconds = self.record.total_seconds
        hours, remainder = divmod(seconds, 3600)
        minutes = (remainder // 60)
        days, hours = divmod(hours, 24)
        parts = []
        if days:
            parts.append(f'{days}d')
        if hours or days:
            parts.append(f'{hours}h')
        parts.append(f'{minutes}m')
        return ' '.join(parts)
