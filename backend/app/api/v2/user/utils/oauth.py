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
