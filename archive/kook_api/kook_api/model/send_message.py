from kook_api.event import MessageType


class SendMsgReq:
    def __init__(self, target_id, content, message_type=MessageType.K_MARKDOWN, quote='', nonce='', temp_target_id=''):
        self.__type = message_type.value
        self.__target_id = target_id
        self.__content = content
        self.__quote = quote
        self.__nonce = nonce
        self.__temp_target_id = temp_target_id

    @property
    def type(self):
        return self.__type

    @property
    def target_id(self):
        return self.__target_id

    @property
    def content(self):
        return self.__content

    @property
    def quote(self):
        return self.__quote

    @property
    def nonce(self):
        return self.__nonce

    @property
    def temp_target_id(self):
        return self.__temp_target_id

    def get_dict(self):
        return {
            'type': self.__type,
            'target_id': self.__target_id,
            'content': self.__content,
            'quote': self.__quote
        }