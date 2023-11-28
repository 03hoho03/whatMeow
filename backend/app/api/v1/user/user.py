from fastapi import Depends, APIRouter, status, UploadFile, File, Request, HTTPException
from sqlalchemy.orm.session import Session

from app.database import get_db
from app.api.schemas import user_schema
from app.api.v1.user import user_utils

router = APIRouter(tags=["User"])


@router.get("/duplicated", status_code=status.HTTP_200_OK)
async def is_duplicated(nickname: str, db: Session = Depends(get_db)):
    if await user_utils.check_duplication(nickname, db):
        return True
    else:
        return False


@router.get("/update/profile", status_code=status.HTTP_200_OK)
async def update_profile_info(request: Request, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        return await user_utils.update_profile_info(decoded_dict.get("id"), db)
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.put("/update/nickname", status_code=status.HTTP_202_ACCEPTED)
async def update_nickname(
    request: Request,
    data: user_schema.UpdateNickname,
    db: Session = Depends(get_db),
):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await user_utils.update_nickname(decoded_dict.get("id"), data.nickname, db):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.put("/update/name", status_code=status.HTTP_202_ACCEPTED)
async def update_name(request: Request, data: user_schema.UpdateName, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await user_utils.update_name(decoded_dict.get("id"), data.name, db):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.put("/update/explain", status_code=status.HTTP_202_ACCEPTED)
async def update_explain(request: Request, data: user_schema.UpdateExplain, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await user_utils.update_explain(decoded_dict.get("id"), data.explain, db):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.put("/update/image", status_code=status.HTTP_202_ACCEPTED)
async def update_image(request: Request, file: UploadFile = File(), db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await user_utils.update_image(decoded_dict.get("id"), file, db):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.get("/notlogined/{nickname}", status_code=status.HTTP_200_OK)
async def load_mypage_nologin(nickname: str, db: Session = Depends(get_db)):
    return await user_utils.load_mypage_utils(nickname, 0, db)


@router.get("/profile/{nickname}", status_code=status.HTTP_200_OK)
async def load_mypage(nickname: str, request: Request, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        return await user_utils.load_mypage_utils(nickname, decoded_dict.get("id"), db)
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.get("/cat", status_code=status.HTTP_200_OK)
async def send_catInfo(request: Request, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        # 고양이 이름, 고양이 식별 아이디
        return await user_utils.send_catInfo(decoded_dict.get("id"), db)
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")
