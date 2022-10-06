from pydantic import BaseModel


class Channel(BaseModel):
    name: str
    platform: str
    channel_id: str

    class Config:
        orm_mode = False
