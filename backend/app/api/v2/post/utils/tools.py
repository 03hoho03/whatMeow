from app.config import settings


async def make_detailed_post(post, user, images, hashtags, comments, statLike):
    _dict = {
        "nickname": user.nickname,
        "writerThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{user.profileImage}",
        "postId": post.id,
        "version": post.version,
        "like": {"count": post.likeCount, "isLike": statLike},
        "content": post.title,
        "createdAt": post.createdAt,
        "images": [f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image.url}" for image in images],
        "hashtags": [hashtag.hashtag for hashtag in hashtags],
        "comments": [
            {
                "commentId": comment.id,
                "comment": comment.comment,
                "nickname": comment.nickname,
                "thumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/user/{comment.uploader}/user.jpg",
            }
            for comment in comments
        ],
    }

    return _dict


async def make_mainfeed_posts(users, posts, images, likes):
    _posts = [
        {
            "nickname": users[i].nickname,
            "writerThumnail": f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/thumnail/{users[i].profileImage}",
            "createdAt": posts[i].createdAt,
            "version": posts[i].version,
            "content": posts[i].title,
            "postId": posts[i].id,
            "images": [
                f"https://{settings.BUCKET_NAME}.s3.ap-northeast-2.amazonaws.com/{image.url}" for image in images[i]
            ],
            "like": {"count": posts[i].likeCount, "isLike": likes[i]},
        }
        for i in range(len(users))
    ]

    _dict = {"posts": _posts, "nextKey": posts[-1].id if len(posts) else 0}

    return _dict
