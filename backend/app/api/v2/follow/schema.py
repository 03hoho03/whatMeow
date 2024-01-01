from pydantic import BaseModel


class FollowReturn(BaseModel):
    isFollowing: bool
    followerCount: int
