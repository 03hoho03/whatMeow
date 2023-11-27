from fastapi import APIRouter, status, Request, Depends, UploadFile, File, Form, HTTPException
from sqlalchemy.orm.session import Session
from typing import Optional

from app.api.schemas import cat_schema
from app.api.v1.cat import cat_utils
from app.database import get_db

router = APIRouter(tags=["Cat"])


@router.post("/add", status_code=status.HTTP_201_CREATED)
async def cat_add(
    request: Request,
    file: UploadFile = File(),
    catname: str = Form(),
    explain: Optional[str] = Form(None),
    db: Session = Depends(get_db),
):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await cat_utils.cat_add_utils(db, file, catname, explain, decoded_dict.get("id")):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.put("/update/image", status_code=status.HTTP_202_ACCEPTED)
async def cat_update(
    request: Request,
    cat_id: int = Form(),
    file: UploadFile = File(),
    db: Session = Depends(get_db),
):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await cat_utils.cat_update_image(db, file, cat_id, decoded_dict.get("id")):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.put("/update/name", status_code=status.HTTP_202_ACCEPTED)
async def cat_update_catname(request: Request, data: cat_schema.CatUpdateName, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await cat_utils.update_catname(data.cat_id, decoded_dict.get("username"), data.catname, db):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.put("/update/explain", status_code=status.HTTP_202_ACCEPTED)
async def cat_update_explain(request: Request, data: cat_schema.CatUpdateExplain, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        if await cat_utils.update_explain(data.cat_id, data.explain, db):
            return {"success": True}
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")


@router.get("/{cat_id}", status_code=status.HTTP_200_OK)
async def cat_info(request: Request, cat_id: int, db: Session = Depends(get_db)):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        return await cat_utils.cat_info(cat_id, decoded_dict.get("username"), db)
    else:
        raise HTTPException(status.HTTP_403_FORBIDDEN, detail="There isn't token")
