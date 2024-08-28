import json

import websockets
from mcdreforged.api.all import *

import kook_api
from kook_api.event import Event, ChannelType, MessageType
from kook_api.constsant.receive_data_key import *
from kook_api.model.send_message import SendMsgReq

__server: PluginServerInterface
__ws_server: websockets


def event_parse(data: str, server: PluginServerInterface, ws_server: websockets):
    global __server, __ws_server
    __server = server
    __ws_server = ws_server
    event_dict: dict = json.loads(data)
    kook_event = Event()
    # Set author id of event
    if event_dict[AUTHOR_ID] == "1":
        # "1" is system message. don't process
        return
    else:
        kook_event.author_id = event_dict[AUTHOR_ID]

    channel_type = event_dict[CHANNEL_TYPE]
    # Set channel type of event
    if channel_type == ChannelType.GROUP.value:
        kook_event.channel_type = ChannelType.GROUP.value

    elif channel_type == ChannelType.PERSON.value:
        kook_event.channel_type = ChannelType.PERSON.value

    elif channel_type == ChannelType.BROADCAST.value:
        kook_event.channel_type = ChannelType.BROADCAST.value

    message_type = event_dict[TYPE]
    # Set message type of event
    if message_type == MessageType.K_MARKDOWN.value:
        parse_k_md_event(kook_event, event_dict)


def parse_k_md_event(event: Event, event_dict: dict):
    # set type to kmarkdown
    event.type = MessageType.K_MARKDOWN.value
    event.content = event_dict[CONTENT]
    event.channel_id = event_dict[TARGET_ID]
    event.msg_id = event_dict[MSG_ID]

    extra = event_dict[EXTRA]

    event.nickname = extra[AUTHOR][NICKNAME]
    event.username = extra[AUTHOR][USERNAME]
    event.raw_content = extra[K_MARKDOWN][RAW_CONTENT]
    # format: username#0123
    event.identified_username = f"{extra[AUTHOR][USERNAME]}#{extra[AUTHOR][IDENTIFY_NUM]}"
    if event.channel_type == ChannelType.GROUP.value:
        event.channel_name = extra[CHANNEL_NAME]
    __server.logger.debug(f"k markdown received:{event}")
    __server.dispatch_event(
        LiteralEvent("kook_api.on_message"), (event.raw_content, event)
    )
