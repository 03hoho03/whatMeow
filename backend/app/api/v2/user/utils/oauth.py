import httpx

from app.config import settings


async def get_result_google(code):
    async with httpx.AsyncClient() as client:
        # Google 토큰 발급
        response = await client.post(
            url="https://oauth2.googleapis.com/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "charset": "utf-8",
                "Cache-Control": "no-cache",
            },
            data={
                "grant_type": "authorization_code",
                "client_id": settings.GOOGLE_CLIENT_ID,
                "client_secret": settings.GOOGLE_CLIENT_SECRET,
                "redirect_uri": settings.GOOGLE_REDIRECT_URI_V2,
                "code": code,
            },
        )
        response = response.json()
        id_token = response.get("id_token")
        result = await client.get(
            url=f"https://oauth2.googleapis.com/tokeninfo?id_token={id_token}",
        )
        result = result.json()

        return result


async def get_result_kakao(code):
    async with httpx.AsyncClient() as client:
        # KaKao 토큰 발급
        response = await client.post(
            url="https://kauth.kakao.com/oauth/token",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "charset": "utf-8",
                "Cache-Control": "no-cache",
            },
            data={
                "grant_type": "authorization_code",
                "client_id": str(settings.KAKAO_CLIENT_ID),
                "client_secret": str(settings.KAKAO_CLIENT_SECRET),
                "redirect_uri": str(settings.KAKAO_REDIRECT_URI_V2),
                "code": str(code),
            },
        )
        response = response.json()
        # 토큰으로 유저 정보 획득
        access_token = response.get("access_token")
        result = await client.post(
            url="https://kapi.kakao.com/v2/user/me",
            headers={
                "Content-Type": "application/x-www-form-urlencoded",
                "Cache-Control": "no-cache",
                "Authorization": "Bearer " + access_token,
            },
            data={},
        )
        result = result.json()

        return result
