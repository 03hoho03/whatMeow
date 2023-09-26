from sqlalchemy import Column, Integer, DateTime, func, String
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base


class BaseMin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())


class User(BaseMin, Base):
    __tablename__ = "user"

    name = Column(String(10), nullable=False)
    nickname = Column(String(20), nullable=True, unique=True)
    email = Column(String(30), nullable=True, unique=True)  # 네이버 로그인 때문에;
    username = Column(String(50), nullable=False, unique=True)
    password = Column(String(255), nullable=True)
    gender = Column(String(5), nullable=True)
    explain = Column(String(50), nullable=True)
    profile_image = Column(String(255), nullable=True)

    cats = relationship("Cat", back_populates="cat_owner")
    posts = relationship("Post", back_populates="post_owner")
    comments = relationship("Comment", back_populates="comment_owner")
    likes = relationship("Like", back_populates="like_owner")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    # Auth Type

    """
    images
    followers
    followings
    """


class Cat(BaseMin, Base):
    __tablename__ = "cat"

    catname = Column(String(20), nullable=False)
    age = Column(Integer, nullable=False)
    gender = Column(String(5), nullable=False)
    explain = Column(String(255), nullable=False)
    breed = Column(String(100), nullable=False)
    owner_id = Column(Integer, ForeignKey("user.id"))

    cat_owner = relationship("User", back_populates="cats")
    """
    images
    """


class Post(BaseMin, Base):
    __tablename__ = "post"

    title = Column(String(50), nullable=False)

    uploader = Column(Integer, ForeignKey("user.id"))

    likes = relationship("Like", back_populates="like_post_owner")
    comments = relationship("Comment", back_populates="comment_post_owner")
    post_owner = relationship("User", back_populates="posts")
    """
    images
    """


class Comment(BaseMin, Base):
    __tablename__ = "comment"

    comment = Column(String(255), nullable=False)
    uploader = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))

    comment_post_owner = relationship("Post", back_populates="comments")
    comment_owner = relationship("User", back_populates="comments")


class Like(BaseMin, Base):
    __tablename__ = "like"

    owner_id = Column(Integer, ForeignKey("user.id"))
    post_id = Column(Integer, ForeignKey("post.id"))

    like_post_owner = relationship("Post", back_populates="likes")
    # 내가 좋아요 눌러놓은 목록들이 필요하면 사용
    like_owner = relationship("User", back_populates="likes")


class Followers(BaseMin, Base):
    __tablename__ = "followers"


class Followings(BaseMin, Base):
    __tablename__ = "followings"


class RefreshToken(BaseMin, Base):
    __tablename__ = "refreshtoken"

    refresh_token = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="refresh_tokens")
