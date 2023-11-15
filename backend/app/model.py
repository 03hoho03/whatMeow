import warnings

from sqlalchemy import Column, Integer, DateTime, func, String, Table
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship

from app.database import Base
from sqlalchemy.exc import SAWarning

warnings.simplefilter("ignore", SAWarning)


class BaseMin:
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, nullable=False, default=func.utc_timestamp())
    updated_at = Column(DateTime, nullable=False, default=func.utc_timestamp(), onupdate=func.utc_timestamp())


followers = Table(
    "followers",
    Base.metadata,
    Column("follower_id", Integer, ForeignKey("user.id")),
    Column("following_id", Integer, ForeignKey("user.id")),
)


class User(BaseMin, Base):
    __tablename__ = "user"

    name = Column(String(10), nullable=False)
    nickname = Column(String(20), nullable=True, unique=True)
    email = Column(String(30), nullable=True)
    password = Column(String(255), nullable=True)
    gender = Column(String(5), nullable=True)
    explain = Column(String(50), nullable=True)
    profile_image = Column(String(255), nullable=True)

    cats = relationship("Cat", back_populates="cat_owner")
    posts = relationship("Post", back_populates="post_owner")
    comments = relationship("Comment", back_populates="comment_owner")
    likes = relationship("Like", back_populates="like_owner")
    refresh_tokens = relationship("RefreshToken", back_populates="user")
    following = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id == followers.c.follower_id",
        secondaryjoin="User.id == followers.c.following_id",
        backref="follower_lst",
        overlaps="follower_lst.follower_lst",
    )
    follower = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id == followers.c.following_id",
        secondaryjoin="User.id == followers.c.follower_id",
        backref="following_lst",
        overlaps="following_lst.following_lst",
    )


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


post_hashtags = Table(
    "post_hashtags",
    Base.metadata,
    Column("post_id", Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True),
    Column("hashtag_id", Integer, ForeignKey("hashtag.id"), primary_key=True),
)


class Post(BaseMin, Base):
    __tablename__ = "post"

    title = Column(String(50), nullable=False)
    uploader_id = Column(Integer, ForeignKey("user.id"))

    likes = relationship("Like", back_populates="like_post_owner", cascade="all,delete")
    comments = relationship("Comment", back_populates="comment_post_owner", cascade="all,delete")
    post_owner = relationship("User", back_populates="posts", foreign_keys=[uploader_id])
    hashtags = relationship("HashTag", secondary=post_hashtags, back_populates="posts")
    images = relationship("Image", back_populates="post", cascade="all,delete")


class Image(BaseMin, Base):
    __tablename__ = "image"

    url = Column(String(100), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))  # 게시물과의 관계 설정

    post = relationship("Post", back_populates="images")


class HashTag(BaseMin, Base):
    __tablename__ = "hashtag"

    hashtag = Column(String(50), nullable=False, unique=True)
    posts = relationship("Post", secondary=post_hashtags, back_populates="hashtags")


class Comment(BaseMin, Base):
    __tablename__ = "comment"

    comment = Column(String(255), nullable=False)
    uploader = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))

    comment_post_owner = relationship("Post", back_populates="comments")
    comment_owner = relationship("User", back_populates="comments")


class Like(BaseMin, Base):
    __tablename__ = "like"

    owner_id = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))

    like_post_owner = relationship("Post", back_populates="likes")
    # 내가 좋아요 눌러놓은 목록들이 필요하면 사용
    like_owner = relationship("User", back_populates="likes")


class RefreshToken(BaseMin, Base):
    __tablename__ = "refreshtoken"

    refresh_token = Column(String(255))
    user_id = Column(Integer, ForeignKey("user.id"))
    user = relationship("User", back_populates="refresh_tokens")
