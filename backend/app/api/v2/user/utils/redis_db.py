from fastapi import HTTPException, status


async def insert_email_code(email, code, redis):
    try:
        await redis.setex(email, 300, code)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail=f"{e} while inserting code to redis"
        )


async def get_email_code(email, code, redis):
    confirm = await redis.get(email)
    confirm = confirm.decode()

    if code == confirm:
        return True
    else:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail="It's too late or Wrong Code")
