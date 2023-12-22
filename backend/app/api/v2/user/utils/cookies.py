async def set_cookie_response(response, token_info):
    response.set_cookie(
        key="accessToken",
        domain="whatmeow.shop",
        samesite="None",
        value=token_info.get("access_token"),
        httponly=True,
        secure=True,
    )
    response.set_cookie(
        key="refreshToken",
        domain="whatmeow.shop",
        samesite="None",
        value=token_info.get("refresh_token"),
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
