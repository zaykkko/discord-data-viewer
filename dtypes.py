from typing import TypedDict, Union, Optional


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


class AppDeveloper(TypedDict):
    id: str
    name: str


class AppExecutable(TypedDict):
    is_launcher: bool
    name: str
    os: str


class AppPublisher(TypedDict):
    id: str
    name: str


class App3rdPartySku(TypedDict):
    distributor: str
    id: str
    sku: str


class App(TypedDict):
    bot_public: Optional[bool]
    bot_require_code_grant: Optional[bool]
    cover_image: Optional[str]
    description: str
    developers: Optional[list[AppDeveloper]]
    executables: list[AppExecutable]
    flags: int
    hook: bool
    icon: Optional[str]
    id: str
    name: str
    publishers: list[AppPublisher]
    rpc_origins: Optional[list[str]]
    splash: Optional[str]
    summary: str
    third_party_skus: list[App3rdPartySku]
    type: int
    verify_key: str


class UserActivity(TypedDict):
    application_id: str
    last_played_at: str
    total_duration: int
    total_discord_sku_duration: int
