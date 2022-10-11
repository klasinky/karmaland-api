from typing import Optional

from pydantic import BaseModel


class Channel(BaseModel):
    name: str
    platform: str
    channel_id: Optional[str] = None

    class Config:
        orm_mode = False
