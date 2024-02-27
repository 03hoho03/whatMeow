from ..utils import tools, redis_db


async def sendEmail(receiverEmail, redis):
    random_code = await tools.make_random_code_for_register()
    await redis_db.insert_email_code(receiverEmail, random_code, redis)
    msg = await tools.make_email_text(receiverEmail, random_code)
    await tools.stmp_connect_and_send(receiverEmail, msg)
