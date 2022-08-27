from pydantic import BaseModel


class Channel(BaseModel):
    name: str
    platform: str

    class Config:
        orm_mode = False
