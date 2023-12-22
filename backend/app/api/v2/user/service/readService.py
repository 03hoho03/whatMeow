from fastapi.responses import JSONResponse, RedirectResponse
from ...application.get_cats_posts__follows_by_user import get_cats_posts_follows_by_user
from ..utils import databases, tools, cookies
from ..schema import GeneralUserReturn


async def nicknameDup(nickname, db):
    return {"duplicated": await databases.is_duplicated(nickname, db)}


async def userLogin(data, response, db):
    user = await databases.find_user_by_email(data.email, db)
    if await tools.is_password_correct(data, user):
        access_token = await tools.create_access_token(user)
        refresh_token = await tools.create_refresh_token(user)
        await databases.update_refresh_token_info(user, refresh_token, db)
        response = JSONResponse(content=GeneralUserReturn(**user.as_dict()).dict())
        response = await cookies.set_cookie_access_token(response, access_token)
        response = await cookies.set_cookie_refresh_token(response, refresh_token)

        return response


async def userLogout(response, id, db):
    if await databases.delete_refreshtoken_info(id, db):
        response = JSONResponse(content={"status": "Logout"})
        response = await cookies.set_cookie_expzero(response)

        return response


async def userTokenRefresh(response, id, db):
    user = await databases.find_user_by_id(id, db)
    access_token = await tools.create_access_token(user)
    response = JSONResponse(content={"status": "New Access Token"})
    response = await cookies.set_cookie_access_token(response, access_token)

    return response


async def googleRedirect():
    url = await tools.get_google_redirect_uri()
    return RedirectResponse(url)


async def kakaoRedirect():
    url = await tools.get_kakao_redirect_url()
    return RedirectResponse(url)


async def readUserProfile(nickname, id, db):
    user = await databases.find_user_by_nickname(nickname, db)
    data = await get_cats_posts_follows_by_user(user, db)
    return await tools.make_return_dict(user, id, data)
