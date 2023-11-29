from fastapi import FastAPI, Request, HTTPException
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.api.v1.auth import auth_utils
from app import api

app = FastAPI()


@app.middleware("http")
async def modify_enpoint(request: Request, call_next):
    if "/profile/" in request.scope["path"]:
        if not request.state.decoded_dict:
            request.scope["path"] = str(request.url.path).replace("profile", "guest")
    response = await call_next(request)
    return response


@app.middleware("http")
async def tag_ifLogined(request: Request, call_next):
    try:
        if "/api/v1/" in request.scope["path"]:
            access_token = request.cookies.get("accessToken")
            refresh_token = request.cookies.get("refreshToken")
            token = access_token if access_token is not None else refresh_token
            if token:
                request.state.decoded_dict = await auth_utils.verify_access_token(token)
            else:
                request.state.decoded_dict = None
        response = await call_next(request)
        return response
    except HTTPException as e:
        return JSONResponse(content={"error": e.detail}, status_code=e.status_code)


app.add_middleware(SessionMiddleware, secret_key="ff29aadd726675a2671da921a53d72e36ec043cdc80056f2f40e602107e6b0f7")
app.add_middleware(
    CORSMiddleware,
    allow_origins={"https://www.whatmeow.shop", "https://local.whatmeow.shop:3001"},
    allow_credentials=True,
    allow_methods={"OPTIONS", "GET", "POST"},
    allow_headers={"*"},
)


@app.on_event("startup")
def on_startup():
    from app import model
    from app.database import engine

    model.Base.metadata.create_all(bind=engine)


app.include_router(api.router)
