from app.model import Cat


async def find_cats_by_owner_id(id, db):
    return db.query(Cat).filter_by(ownerId=id).all()
