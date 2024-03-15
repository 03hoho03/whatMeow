from fastapi.responses import RedirectResponse
from ..utils import databases, images, tools, oauth, cookies


async def userRegister(data, db):
    password = await tools.create_hashed_password(data.password)
    user = await databases.add_generaluser(data, password, db)
    url = await images.upload_default_image(user.id)
    user.profileImage = url

    db.commit()

    return user


async def googleSocialLogin(response, code, db):
    result = await oauth.get_result_google(code)
    user = await databases.find_user_by_email_without_exception(result.get("email"), db)
    if user:
        access_token = await tools.create_access_token(user)
        refresh_token = await tools.create_refresh_token(user)
        await databases.update_refresh_token_info(user, refresh_token, db)
        response = RedirectResponse(url=f"https://www.whatmeow.shop/?nickname={user.nickname}")
        response = await cookies.set_cookie_access_token(response, access_token)
        response = await cookies.set_cookie_refresh_token(response, refresh_token)

        return response
    else:
        nickname = await databases.get_random_nickname(db)
        new_user = await databases.add_google_user(result, nickname, db)
        url = await images.upload_default_image(new_user.id)
        new_user.profileImage = url
        access_token = await tools.create_access_token(new_user)
        refresh_token = await tools.create_refresh_token(new_user)
        await databases.update_refresh_token_info(new_user, refresh_token, db)
        response = RedirectResponse(url=f"https://www.whatmeow.shop/?nickname={nickname}")
        response = await cookies.set_cookie_access_token(response, access_token)
        response = await cookies.set_cookie_refresh_token(response, refresh_token)

        db.commit()
        return response


async def kakaoSocialLogin(response, code, db):
    result = await oauth.get_result_kakao(code)
    user = await databases.find_user_by_kakao_id(result.get("id"), db)
    if user:
        access_token = await tools.create_access_token(user)
        refresh_token = await tools.create_refresh_token(user)
        await databases.update_refresh_token_info(user, refresh_token, db)
        response = RedirectResponse(url=f"https://www.whatmeow.shop/?nickname={user.nickname}")
        response = await cookies.set_cookie_access_token(response, access_token)
        response = await cookies.set_cookie_refresh_token(response, refresh_token)

        return response
    else:
        nickname = await databases.get_random_nickname(db)
        new_user = await databases.add_kakao_user(
            result, result.get("properties"), result.get("kakao_account"), nickname, db
        )
        url = await images.upload_default_image(new_user.id)
        new_user.profileImage = url
        access_token = await tools.create_access_token(new_user)
        refresh_token = await tools.create_refresh_token(new_user)
        await databases.update_refresh_token_info(new_user, refresh_token, db)
        response = RedirectResponse(url=f"https://www.whatmeow.shop/?nickname={nickname}")
        response = await cookies.set_cookie_access_token(response, access_token)
        response = await cookies.set_cookie_refresh_token(response, refresh_token)

        db.commit()
        return response
