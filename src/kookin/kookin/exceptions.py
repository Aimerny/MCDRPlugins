class ParseMetException(Exception):
    def __init__(self, content:str):
        super().__init__(content)
        self.content = f'@ target string "{content}" is invalid'


class InvalidParamException(Exception):
    def __init__(self, msg:str):
        super().__init__(msg)
        self.msg = msg
