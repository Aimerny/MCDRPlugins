import json
from typing import Optional

import websockets
import requests
from mcdreforged.api.all import *

import kook_api.constsant.api_uri as api_uri
from kook_api.event import Event, MessageType
from kook_api.model.send_message import SendMsgReq
from kook_api.model.channels_info_resp import ChannelsInfoResp,ChannelInfo


class KookApi:
    _ws_server: websockets
    _mcdr_server: PluginServerInterface
    _api_host: str
    _api_port: int
    _headers = {
        'Content-Type': 'application/json'
    }

    def __init__(self, mcdr_server, api_host, api_port):
        self._mcdr_server = mcdr_server
        self._api_host = api_host
        self._api_port = api_port

    def _get_api_address(self) -> str:
        return f"{self._api_host}:{self._api_port}"

    def _get_api_url(self, uri: str) -> str:
        return f"http://{self._api_host}:{self._api_port}{uri}"

    def _logger(self):
        return self._mcdr_server.logger

    def send_message_to_channel(self, req: SendMsgReq):
        body = json.dumps(req.get_dict())
        resp = requests.post(url=self._get_api_url(api_uri.MESSAGE_SEND), data=body, headers=self._headers)
        self._logger().debug(f"A message send to kook bot:{req.content}, target channel is:{req.target_id}")
        if resp.status_code != 200:
            self._logger().warning(f"Send message failed! Exception response is :'{resp.content}'")

    def search_channels(self, search_key: str) -> Optional[ChannelsInfoResp]:
        params = {
            "searchKey": search_key
        }
        resp = requests.get(url=self._get_api_url(api_uri.CHANNEL_SEARCH), params=params, headers=self._headers)
        self._logger().debug(f"query channels msg from kook. search key is :{search_key}")
        if resp.status_code != 200:
            self._logger().error(f"query channel msg failed!")
            return None
        channels_info = ChannelsInfoResp(**json.loads(resp.content))
        return channels_info

    def reply(self, event: Event, content: str):
        req = SendMsgReq(target_id=event.channel_id, content=content, quote=event.msg_id)
        self.send_message_to_channel(req)
