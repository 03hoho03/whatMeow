from app.model import Post


async def find_posts_by_uploader_id(id, db):
    return db.query(Post).filter_by(uploader_id=id).all()
