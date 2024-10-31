from redis import asyncio as aioredis

from app.config import settings

redis = aioredis.from_url(settings.REDIS_URL)


async def increment_matches(user_id: int, limit: int = 5) -> bool:
    key = f"matches_count:{user_id}"
    count = await redis.incr(key)
    if count == 1:
        await redis.expire(key, 86400)
    return count > limit
