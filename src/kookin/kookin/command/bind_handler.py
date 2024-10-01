# from typing import List
#
# from mcdreforged.api.all import *
#
# from kook_api.event import Event
# from kookin.command.command_handler import CommandHandler
# from kookin.config import Config, UserInfo, Data
# from kook_api.api import KookApi
# from kookin.exceptions import ParseMetException, InvalidParamException
# from kookin.util import save_file, get_all_admin_channel_ids
# from kookin.constant import DATA_FILE
#
#
# class BindCommandHandler(CommandHandler):
#     def __init__(self, server: PluginServerInterface, config: Config, data: Data, kook_api: KookApi):
#         super().__init__(server, config, data, kook_api)
#
#     def handle(self, command_nodes: List[str], event: Event):
#         # 校验是否具备管理权限
#         user_id = event.author_id
#         identified_username = event.identified_username
#         if identified_username in self.__config.admins or event.channel_id in get_all_admin_channel_ids():
#             # /bind list
#             if len(command_nodes) == 2 and command_nodes[1] == 'list':
#                 # 获取当前用户列表
#                 user_list = self.__data.bound_list
#                 resp = '===已绑定的用户列表===\n---\n| user | player |\n| ---- | ---- |\n'
#                 for info_dict in user_list:
#                     user_info = UserInfo.deserialize(info_dict)
#                     resp += f'| {user_info.username} | {user_info.player_name} |\n'
#                 resp += '| ---- | ---- |'
#                 return self.__kook_api.reply(event, resp)
#             elif len(command_nodes) == 3:
#                 # /bind clear <player_name>
#                     try:
#                         if command_nodes[1] == 'clear':
#                             target_user_id = UserInfo.parse_at(command_nodes[2])
#                             exist_user = self.__data.find_user_by_id(target_user_id)
#                             if exist_user is not None:
#                                 self.__data.clear_user(exist_user)
#                                 save_file(self.__data, DATA_FILE, self.__server)
#                                 self.__kook_api.reply(event, f"已解除{UserInfo.at(target_user_id)}的绑定")
#
#                     except InvalidParamException as e:
#                         self.__kook_api.reply(event, f"内部错误，错误信息:{e.msg}")
#                     except ParseMetException as e:
#                         self.__kook_api.reply(event, e.content)
#
#         # 非管理员只能主动绑定
#         # /bind <player_name>
#         if len(command_nodes) == 2:
#             if command_nodes[1] == 'list':
#                 self.__kook_api.reply(event, f"{UserInfo.at(user_id)}仅管理员可用")
#                 return
#             player_name = command_nodes[1]
#             user_id = event.author_id
#             bound_list = self.__data.bound_list
#             exist_user = self.__data.find_user_by_id(user_id)
#             if exist_user is not None:
#                 self.__server.logger.warning(f"{UserInfo.at(user_id)}已经绑定Id为:{exist_user.player_name}")
#                 return self.__kook_api.reply(event, f"{UserInfo.at(user_id)}你已经绑定Id为:{exist_user.player_name}，请联系管理员解绑")
#
#             user_info = UserInfo(event.username, user_id, player_name)
#             bound_list.append(user_info.serialize())
#             save_file(self.__data, DATA_FILE, self.__server)
#             return self.__kook_api.reply(event, f"已成功绑定Id:{player_name}")
#
