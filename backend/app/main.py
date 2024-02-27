from fastapi import FastAPI, Request, HTTPException, status
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware
from jose import jwt
from jose.exceptions import ExpiredSignatureError

from app.config import settings
from app import api


async def verify_token(token, type, isLogout=None):
    key = settings.SECRET_ACCESS_KEY if type == "access" else settings.SECRET_REFRESH_KEY
    try:
        jwt_dict = jwt.decode(token, key, settings.ALGORITHM)
        if jwt_dict:
            return jwt_dict
    except ExpiredSignatureError:
        if isLogout:
            return jwt_dict
        else:
            raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Expired")


app = FastAPI()


@app.middleware("http")
async def tag_ifLogined(request: Request, call_next):
    try:
        if "/api" in request.scope["path"]:
            access_token = request.cookies.get("accessToken")
            refresh_token = request.cookies.get("refreshToken")

            if "/token/refresh" in request.scope["path"]:
                request.state.refresh_token = await verify_token(refresh_token, "refresh") if refresh_token else None
            elif "/logout" in request.scope["path"]:
                request.state.access_token = (
                    await verify_token(access_token, "access", "Logout") if access_token else None
                )
            else:
                request.state.access_token = await verify_token(access_token, "access") if access_token else None

        response = await call_next(request)

        return response
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


app.add_middleware(SessionMiddleware, secret_key="ff29aadd726675a2671da921a53d72e36ec043cdc80056f2f40e602107e6b0f7")
app.add_middleware(
    CORSMiddleware,
    allow_origins={"https://www.whatmeow.shop", "https://local.whatmeow.shop:3001"},
    allow_credentials=True,
    allow_methods={"OPTIONS", "GET", "POST", "DELETE", "PUT"},
    allow_headers={"*"},
)


@app.on_event("startup")
def on_startup():
    from app import model
    from app.database import engine, get_redis

    model.Base.metadata.create_all(bind=engine)
    app.state.redis = get_redis()


@app.on_event("shutdown")
async def off_shutdown():
    await app.state.redis.close()


app.include_router(api.router)
