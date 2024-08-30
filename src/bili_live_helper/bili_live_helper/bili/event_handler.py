import logging
from abc import ABC,abstractmethod
from typing import List, Dict

from bili_live_helper.bili.live_event import LiveEvent, DanmuInfo


class EventReceiver(ABC):
    @abstractmethod
    def forward_danmu(self, danmu: DanmuInfo):
        pass


class EventHandler:
    __logger: logging.Logger
    __receivers: Dict[str, EventReceiver]

    def __init__(self, logger):
        self.__logger = logger
        self.__receivers = {}

    def get_receiver(self, key: str):
        return self.__receivers.get(key, None)

    def put_receiver(self, key: str, receiver: EventReceiver):
        self.__receivers[key] = receiver

    def remove_receiver(self, key: str) -> EventReceiver:
        receiver = self.__receivers.get(key)
        if receiver is not None:
            del self.__receivers[key]
        return receiver

    def handle_event(self, event: LiveEvent):
        self.__logger.debug(f'received event: {event}')
        data = event.data
        if event.type != 'DANMU_MSG':
            self.__logger.warning('not support event type: {}', event.type)
            return
        # skip msg from self
        if data.send_from_me:
            return
        if len(self.__receivers.keys()) == 0:
            self.__logger.warning('forward skip! receivers is empty')
        for key, receiver in self.__receivers.items():
            receiver.forward_danmu(data)
