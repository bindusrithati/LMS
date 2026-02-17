from fastapi import Request, HTTPException, status
from app.utils.redis_client import redis_client


def rate_limiter(key_prefix: str, limit: int, window: int):
    async def limiter(request: Request):
        user = getattr(request.state, "user", None)

        identifier = user.id if user else request.client.host
        redis_key = f"rate:{key_prefix}:{identifier}"
        try:

            current = await redis_client.incr(redis_key)

            if current == 1:
                await redis_client.expire(redis_key, window)

            if current > limit:
                raise HTTPException(
                    status_code=status.HTTP_429_TOO_MANY_REQUESTS,
                    detail="Too many requests. Please try again later.",
                )
        except Exception:
            pass

    return limiter
