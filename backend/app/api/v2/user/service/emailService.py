from ..utils import tools


async def sendEmail(receiverEmail):
    random_code = await tools.make_random_code_for_register()
    msg = await tools.make_email_text(receiverEmail, random_code)
    await tools.stmp_connect_and_send(receiverEmail, msg)
