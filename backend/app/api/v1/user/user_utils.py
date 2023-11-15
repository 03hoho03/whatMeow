from app import model
from sqlalchemy.orm.exc import NoResultFound


async def check_duplication(nickname, db):
    try:
        db.query(model.User).filter_by(nickname=nickname).first()
        return False
    except NoResultFound:
        return True
