from typing import List
import json


class ChannelInfo:
    def __init__(self, channel_id: str, channel_name: str, guild_id: str, guild_name: str):
        self.__channel_id = channel_id
        self.__channel_name = channel_name
        self.__guild_id = guild_id
        self.__guild_name = guild_name

    @property
    def channel_id(self) -> str:
        return self.__channel_id

    @property
    def channel_name(self) -> str:
        return self.__channel_name

    @property
    def guild_id(self) -> str:
        return self.__guild_id

    @property
    def guild_name(self) -> str:
        return self.__guild_name

    def __repr__(self):
        return (f"ChannelInfo(channel_id={self.__channel_id},channel_name={self.__channel_name}"
                f",guild_id={self.__guild_id},guild_name={self.__guild_name})")


class ChannelsInfoResp:
    def __init__(self, code: int, message: str, channels: List[ChannelInfo]):
        self.__code = code
        self.__message = message
        self.__channels = channels

    @property
    def code(self) -> int:
        return self.__code

    @property
    def message(self) -> str:
        return self.__message

    @property
    def channels(self) -> List[ChannelInfo]:
        return self.__channels
