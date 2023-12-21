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
