import logging
from typing import AsyncGenerator, Optional
import redis.asyncio as aioredis
from redis.asyncio.connection import ConnectionPool
from app.core.config import settings

logger = logging.getLogger("intellitwin.redis")

class EnterpriseRedisClient:
    def __init__(self):
        self.pool: Optional[ConnectionPool] = None

    def initialize_pool(self) -> None:
        try:
            self.pool = ConnectionPool.from_url(
                settings.REDIS_URL,
                max_connections=50,
                socket_timeout=5.0,
                socket_connect_timeout=5.0,
                retry_on_timeout=True,
                decode_responses=True
            )
            logger.info("Redis Enterprise connection pool established.")
        except Exception as e:
            logger.error(f"Redis initialization failed: {e}")
            raise e

    async def get_session(self) -> AsyncGenerator[aioredis.Redis, None]:
        if not self.pool:
            self.initialize_pool()
        client = aioredis.Redis(connection_pool=self.pool)
        try:
            yield client
        finally:
            await client.aclose()

    async def close_pool(self) -> None:
        if self.pool:
            await self.pool.disconnect()
            logger.info("Redis connection pool disconnected cleanly.")

redis_client = EnterpriseRedisClient()