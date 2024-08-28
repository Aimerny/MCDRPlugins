from mcdreforged.utils.serializer import Serializable


class Config(Serializable):
    # kook代理host
    kook_host:str = "0.0.0.0"
    # kook代理port
    kook_port:int = 9000
    # api端口
    api_port:int = 9001
