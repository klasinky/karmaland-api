from typing import Optional

from pydantic import BaseModel


class Channel(BaseModel):
    name: str
    platform: str
    channel_id: Optional[str] = None

    class Config:
        orm_mode = False


class ChannelInfo(BaseModel):
    user_name: str
    title: str
    platform: str
    viewer_count: Optional[int] = None

    class Config:
        orm_mode = False