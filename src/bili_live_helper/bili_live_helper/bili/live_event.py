import json


class DanmuInfo:
    extra: dict
    send_from_me: bool
    mode: int
    dm_type: int
    font_size: int
    player_mode: int
    content: str
    user: str
    user_uid: int

    @classmethod
    def from_event(cls, event_info: dict) -> 'DanmuInfo':
        res = cls()
        res.extra = json.loads(event_info[0][15]["extra"])
        res.send_from_me = res.extra["send_from_me"]
        res.mode = res.extra["mode"]
        res.dm_type = res.extra["dm_type"]
        res.font_size = res.extra["font_size"]
        res.player_mode = res.extra["player_mode"]

        res.content = event_info[1]
        res.user_uid = event_info[2][0]
        res.user = event_info[2][1]
        return res


class LiveEvent:
    room_display_id: int
    room_real_id: int
    type: str
    data: DanmuInfo

    @classmethod
    def parse_from(cls, event: dict) -> 'LiveEvent':
        res = LiveEvent()
        # parse DANMU event
        if event["type"] == "DANMU_MSG":
            res.type = "DANMU_MSG"
            res.room_display_id = event["room_display_id"]
            res.room_real_id = event["room_real_id"]
            res.data = DanmuInfo.from_event(event["data"]["info"])
            return res
        else:
            raise Exception("not supported yet")