from fastapi import APIRouter, HTTPException, status, Request, UploadFile, File

from app.api.v1.ai import ai_utils

router = APIRouter(tags=["AI"])


@router.post("", status_code=status.HTTP_200_OK)
async def basic_ai(request: Request, file: UploadFile = File()):
    decoded_dict = request.state.decoded_dict
    if decoded_dict:
        cat_breeds = await ai_utils.predict_breed(file)
        if cat_breeds:
            return cat_breeds
        else:
            raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="No Cat Detected in Image")
    else:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="There isn't token")