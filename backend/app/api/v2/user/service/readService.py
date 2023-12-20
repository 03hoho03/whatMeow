from ..utils import databases


async def nicknameDup(nickname, db):
    return {"duplicated": await databases.is_duplicated(nickname, db)}
