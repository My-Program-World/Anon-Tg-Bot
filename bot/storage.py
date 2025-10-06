from aiogram.fsm.storage.redis import RedisStorage
from redis.asyncio import Redis

redis_storage = RedisStorage(Redis())