from fastapi import HTTPException, status


async def insert_email_code(email, code, redis):
    try:
        await redis.setex(email, 10, code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while inserting code to redis"
        )
