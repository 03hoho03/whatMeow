from fastapi.responses import JSONResponse
from ..utils import databases, tools, cookies
from ..schema import GeneralUserReturn


async def nicknameDup(nickname, db):
    return {"duplicated": await databases.is_duplicated(nickname, db)}


async def userLogin(data, response, db):
    user = await databases.find_user_by_email(data.email, db)
    if await tools.is_password_correct(data, user):
        token_info = await tools.create_access_token(user, db)
        await databases.update_refresh_token_info(user, token_info)
        response = JSONResponse(content=GeneralUserReturn(**user.as_dict()).dict())
        response = await cookies.set_cookie_response(response, token_info)

        return response
