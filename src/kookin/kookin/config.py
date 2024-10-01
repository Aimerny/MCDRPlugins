import re

from mcdreforged.api.all import *
from typing import List

from kookin.exceptions import ParseMetException, InvalidParamException


class ChannelInfo(Serializable):
    channel_name: str = ''
    channel_id: str = ''

    def __init__(self, channel_name, channel_id, **kwargs):
        super().__init__(**kwargs)
        self.channel_id = channel_id
        self.channel_name = channel_name


class UserInfo(Serializable):
    username: str = ''
    user_id: str = ''
    player_name: str = ''

    def __init__(self, username=None, user_id=None, player_name=None, **kwargs):
        super().__init__(**kwargs)
        self.username = username
        self.user_id = user_id
        self.player_name = player_name

    def __setattr__(self, key, value):
        self.__dict__[key] = value

    @staticmethod
    def parse_at(content: str) -> str:
        pattern = r'\(met\)([0-9]+?)\(met\)'
        matcher = re.match(pattern, content)
        if matcher is None:
            raise ParseMetException(content)
        else:
            return matcher.group(1)

    # @成员
    @staticmethod
    def at(user_id: str) -> str:
        return f'(met){user_id}(met)'


class Config(Serializable):
    # Bot Token
    token: str = 'your token'
    # 指令前缀,允许配置多个
    prefixes: List[str] = [
        '/'
    ]
    # 管理频道列表
    admin_channel: List[dict] = [ChannelInfo('机器人管理频道', '1145141919810').serialize()]
    # 公共频道列表
    public_channel: List[dict] = [ChannelInfo('服务器成员公共频道', '123456').serialize()]
    # 聊天板同步频道
    sync_chat_channel: List[dict] = [ChannelInfo('服务器聊天同步频道', '23333').serialize()]
    # 管理员列表(使用username#唯一标识号)
    admins: List[str] = ['home#114514']
    server_name: str = 'Survival'


class Data(Serializable):
    # 成员绑定列表
    bound_list: List[dict] = []

    def find_user_by_id(self, user_id) -> UserInfo:
        for user in self.bound_list:
            if user['user_id'] == user_id:
                return UserInfo.deserialize(user)

    def clear_user(self, user=None, user_id=None):
        if user is None and user_id is None:
            raise InvalidParamException(f'Clear user param is None!')
        # 优先使用user_id，覆盖掉传入的user
        elif user_id is not None:
            user = self.find_user_by_id(user_id)
        # 去掉该user
        self.bound_list = list(filter(lambda d: d != serialize(user), self.bound_list))
