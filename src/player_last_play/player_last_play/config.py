from dataclasses import dataclass, field
from typing import List

from mcdreforged.api.all import Serializable


@dataclass
class Config(Serializable):
    # 一周内没上线属于很活跃
    active: int = 7
    # 两周内没上线属于较为一般
    normal: int = 14
    # 三周内没上线属于基本不活跃,超过三周属于潜水
    inactive: int = 21
    # 是否倒序查询,默认从近到远
    reverse: bool = True
    # 分页查询的大小,默认10
    pageSize: int = 10
    # 忽略玩家正则列表
    ignorePlayerRegexes: List[str] = field(default_factory=lambda: ['^bot_.*$', '^Bot_.*$'])
    # 是否只统计白名单内玩家
    only_whitelist_player: bool = False

    def validate(self) -> None:
        """验证配置有效性"""
        if self.active <= 0:
            raise ValueError("active must be positive")
        if self.normal <= self.active:
            raise ValueError("normal must be greater than active")
        if self.inactive <= self.normal:
            raise ValueError("inactive must be greater than normal")
        if self.pageSize <= 0:
            raise ValueError("pageSize must be positive") 