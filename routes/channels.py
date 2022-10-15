from typing import List

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from config.env import get_settings
from config.redis import get_redis
from redis_client.connection import RedisConnection
from schemas.channels import Channel, ChannelInfo
from settings import Settings
from utils.db import get_db
from utils.request import check_users_list

app = APIRouter()


def my_key_builder(
        func,
        channels: List[Channel],
        *args,
        **kwargs,
):
    # Create a key from the arguments passed to the function
    cache_key = f'{func.__name__}{"-".join([channel.name for channel in channels])}'
    return cache_key


@app.get("/")
def index():
    return {"message": "Hello World from channels"}


@app.post('/', response_model=list)
async def check_users(channels: List[Channel], db: Session = Depends(get_db),
                      settings: Settings = Depends(get_settings), redis: RedisConnection = Depends(get_redis)) \
        -> List[ChannelInfo]:
    cache_key = my_key_builder(check_users, channels)
    result = redis.get(cache_key)
    if not result:
        result = await check_users_list(channels, db, settings)
        redis.set(cache_key, result, expire=300)

    return result
