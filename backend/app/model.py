from sqlalchemy import Column, Integer, DateTime, func, String, Table
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.exc import SAWarning
import warnings

from app.database import Base

warnings.filterwarnings("ignore", category=SAWarning)


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
    nickname = Column(String(20), nullable=False, unique=True)
    username = Column(String(20), nullable=False, unique=True)
    kakao_id = Column(String(20), nullable=True, unique=True)
    email = Column(String(30), nullable=True, unique=True)
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
        overlaps="follower_lst,following_lst",
    )
    follower = relationship(
        "User",
        secondary=followers,
        primaryjoin="User.id == followers.c.following_id",
        secondaryjoin="User.id == followers.c.follower_id",
        backref="following_lst",
        overlaps="following_lst,follower_lst",
    )

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Follow(Base, BaseMin):
    __tablename__ = "follow"

    fromUserId = Column(Integer, ForeignKey("user.id"))
    toUserId = Column(Integer, ForeignKey("user.id"))

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class PostCats(Base, BaseMin):
    __tablename__ = "postcats"
    postId = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    catId = Column(Integer, ForeignKey("cat.id", ondelete="CASCADE"))


class PostHashTag(Base, BaseMin):
    __tablename__ = "posthashtag"
    postId = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    hashtagId = Column(Integer, ForeignKey("hashtag.id"))


class Cat(BaseMin, Base):
    __tablename__ = "cat"

    catname = Column(String(20), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(5), nullable=True)
    cat_hashtags = Column(String(50), nullable=True)
    explain = Column(String(255), nullable=True)
    breed = Column(String(100), nullable=True)
    owner_id = Column(Integer, ForeignKey("user.id"))
    image = Column(String(100), nullable=False)

    cat_owner = relationship("User", back_populates="cats")


class Post(BaseMin, Base):
    __tablename__ = "post"

    title = Column(String(50), nullable=False)
    uploader_id = Column(Integer, ForeignKey("user.id"))

    likes = relationship("Like", back_populates="like_post_owner", cascade="all,delete")
    comments = relationship("Comment", back_populates="comment_post_owner", cascade="all,delete")
    post_owner = relationship("User", back_populates="posts", foreign_keys=[uploader_id])
    images = relationship("Image", back_populates="post", cascade="all,delete")


class Image(BaseMin, Base):
    __tablename__ = "image"

    url = Column(String(255), nullable=False)
    post_id = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))  # 게시물과의 관계 설정

    post = relationship("Post", back_populates="images")


class HashTag(BaseMin, Base):
    __tablename__ = "hashtag"

    hashtag = Column(String(50), nullable=False, unique=True)


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


class CatFeature(Base):
    __tablename__ = "catfeature"

    cat_breed = Column(String(15), primary_key=True)
    feature = Column(String(255))
