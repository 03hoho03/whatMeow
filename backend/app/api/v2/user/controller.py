from aioredis import Redis
from fastapi import APIRouter, Depends, status, Response, Request, BackgroundTasks
from sqlalchemy.orm.session import Session

from app.database import get_db, get_redis
from . import schema
from .service import writeService, readService, emailService

router = APIRouter(tags=["UserV2"])


@router.post("/register", status_code=status.HTTP_201_CREATED, response_model=schema.GeneralUserReturn)
async def register(data: schema.GeneralUserAdd, db: Session = Depends(get_db)):
    return await writeService.userRegister(data, db)


@router.get("/duplicated", status_code=status.HTTP_200_OK)
async def checkDup(nickname: str, db: Session = Depends(get_db)):
    return await readService.nicknameDup(nickname, db)


@router.post("/login", status_code=status.HTTP_200_OK)
async def login(response: Response, data: schema.GeneralUserLogin, db: Session = Depends(get_db)):
    return await readService.userLogin(data, response, db)


@router.get("/logout", status_code=status.HTTP_204_NO_CONTENT)
async def logout(response: Response, request: Request, db: Session = Depends(get_db)):
    access_token = request.state.access_token
    return await readService.userLogout(response, access_token.get("id"), db)


@router.get("/token/refresh", status_code=status.HTTP_200_OK)
async def refresh(response: Response, request: Request, db: Session = Depends(get_db)):
    refresh_token = request.state.refresh_token
    return await readService.userTokenRefresh(response, refresh_token.get("id"), db)


@router.get("/login/google")
async def google():
    return await readService.googleRedirect()


@router.get("/login/google/callback")
async def googleLogin(response: Response, code: str | None = None, db: Session = Depends(get_db)):
    return await writeService.googleSocialLogin(response, code, db)


@router.get("/login/kakao")
async def kakao():
    return await readService.kakaoRedirect()


@router.get("/login/kakao/callback")
async def kakaoLogin(response: Response, code: str | None = None, db: Session = Depends(get_db)):
    return await writeService.kakaoSocialLogin(response, code, db)


@router.get("/profile/{nickname}")
async def userProfile(nickname: str, request: Request, db: Session = Depends(get_db)):
    access_token = request.state.access_token
    return await readService.readUserProfile(nickname, access_token.get("id") if access_token else None, db)


@router.get("/cat", status_code=status.HTTP_200_OK)
async def send_catInfo(request: Request, db: Session = Depends(get_db)):
    access_token = request.state.access_token
    return await readService.readCatInfo(access_token.get("id"), db)


@router.post("/email-confirm", status_code=status.HTTP_200_OK)
async def sendEmail(data: schema.GeneralUserBase, background_tasks: BackgroundTasks, redis: Redis = Depends(get_redis)):
    background_tasks.add_task(emailService.sendEmail, data.email, redis)

    return {"message": "Server started to send confirm-email"}
