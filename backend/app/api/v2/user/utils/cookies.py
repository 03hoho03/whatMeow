async def set_cookie_access_token(response, access_token):
    response.set_cookie(
        key="accessToken",
        domain="whatmeow.shop",
        samesite="None",
        value=access_token,
        httponly=True,
        secure=True,
    )

    return response


async def set_cookie_refresh_token(response, refresh_token):
    response.set_cookie(
        key="refreshToken",
        domain="whatmeow.shop",
        samesite="None",
        value=refresh_token,
        httponly=True,
        secure=True,
    )

    return response


async def set_cookie_expzero(response):
    response.set_cookie(
        key="accessToken",
        domain="whatmeow.shop",
        samesite="None",
        value="",
        httponly=True,
        secure=True,
        max_age=1,
    )

    response.set_cookie(
        key="refreshToken",
        domain="whatmeow.shop",
        samesite="None",
        value="",
        httponly=True,
        secure=True,
        max_age=1,
    )
    return response
