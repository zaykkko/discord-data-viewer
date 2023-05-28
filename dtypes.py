from typing import TypedDict, Union


class Guild(TypedDict):
    id: str
    name: str


class ChannelInfo(TypedDict):
    id: str
    type: int
    name: Union[str, None]
    recipients: Union[list[str], None]
    icon_hash: Union[str, None]
    guild: Union[Guild, None]
