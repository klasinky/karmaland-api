from typing import List, Optional

from redis import Redis
import pickle
from schemas.channels import ChannelInfo


class RedisConnection:
    def __init__(self, host, port, db, password):
        self.host = host
        self.port = port
        self.db = db
        self.connection : Optional[Redis] = None
        self.password = password

    def connect(self):
        self.connection = Redis(host=self.host, port=self.port, db=self.db, password=self.password)
        self.connection.connection_pool.make_connection()

    def get_connection(self):
        if self.connection is None:
            self.connect()
        return self.connection

    def close_connection(self):
        self.connection.close()

    def set(self, key: str, data: List[ChannelInfo], expire: int = 60):
        parse_data = pickle.dumps(data)
        self.connection.set(name=key, value=parse_data)
        self.connection.expire(name=key, time=60)

    def get(self, key: str):
        data = self.connection.get(key)
        if data:
            return pickle.loads(data)
        return None

# Path: redis_client/redis_client.py
