from app import model
from fastapi import HTTPException, status

# from sqlalchemy.orm.exc import NoResultFound


async def cat_add_utils(db, data, user_id):
    try:
        row = model.Cat(**data.dict(), owner_id=user_id)
        db.add(row)
        db.commit()

        return True
    except Exception as e:
        print(e)
        raise HTTPException(status_code=status.HTTP_422_UNPROCESSABLE_ENTITY, detail="Error Occured")
