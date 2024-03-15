from ..post.utils import databases as postdb
from ..user.utils import databases as userdb
from ..comment.utils import databases as commentdb
from ..like.utils import databases as likedb


async def get_posts_users_hashtags_by_post_id(userId, postId, db):
    post = await postdb.find_post_by_post_id(postId, db)
    user = await userdb.find_user_by_id(post.uploaderId, db)
    images = await postdb.find_urls_by_post_id(postId, db)
    hashtagIds = await postdb.find_hashtagids_by_post_id(postId, db)
    hashtags = await postdb.find_hashtags_by_hashtagids(hashtagIds, db)
    comments = await commentdb.find_commets_by_post_id(postId, db)
    statLike = await likedb.is_like(userId, postId, db)

    return post, user, images, hashtags, comments, statLike
