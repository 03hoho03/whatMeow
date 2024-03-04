from sqlalchemy import Column, Integer, DateTime, func, String, Index
from sqlalchemy.sql.schema import ForeignKey
from sqlalchemy.exc import SAWarning
import warnings

from app.database import Base

warnings.filterwarnings("ignore", category=SAWarning)


class BaseMin:
    id = Column(Integer, primary_key=True, index=True)
    createdAt = Column(DateTime, nullable=False, default=func.now())
    updatedAt = Column(DateTime, nullable=False, default=func.now(), onupdate=func.now())


class User(BaseMin, Base):
    __tablename__ = "user"

    name = Column(String(10), nullable=False)
    nickname = Column(String(20), nullable=False, unique=True)
    kakaoId = Column(String(20), nullable=True, unique=True)
    email = Column(String(30), nullable=True, unique=True)
    password = Column(String(255), nullable=True)
    gender = Column(String(5), nullable=True)
    explain = Column(String(50), nullable=True)
    profileImage = Column(String(255), nullable=True)

    __table_args__ = (Index("idx_nickname", "nickname"),)
    __table_args__ = (Index("idx_email", "email"),)
    __table_args__ = (Index("idx_kakao_id", "kakaoId"),)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class Follow(Base, BaseMin):
    __tablename__ = "follow"

    fromUserId = Column(Integer, ForeignKey("user.id"))
    toUserId = Column(Integer, ForeignKey("user.id"))

    __table_args__ = (Index("idx_fromUserId_toUserId", "fromUserId", "toUserId"),)

    def as_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}


class PostCats(Base, BaseMin):
    __tablename__ = "postcats"
    postId = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    catId = Column(Integer, ForeignKey("cat.id", ondelete="CASCADE"))

    __table_args__ = (Index("idx_postId_catId", "postId", "catId"),)


class PostHashTag(Base, BaseMin):
    __tablename__ = "posthashtag"
    postId = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))
    hashtagId = Column(Integer, ForeignKey("hashtag.id"))

    __table_args__ = (Index("idx_postId_hashtagId", "postId", "hashtagId"),)


class Cat(BaseMin, Base):
    __tablename__ = "cat"

    catName = Column(String(20), nullable=False)
    age = Column(Integer, nullable=True)
    gender = Column(String(5), nullable=True)
    explain = Column(String(255), nullable=True)
    breed = Column(String(100), nullable=True)
    ownerId = Column(Integer, ForeignKey("user.id"))
    image = Column(String(100), nullable=True)

    __table_args__ = (Index("idx_owner_id", "ownerId"),)


class CatHashTag(Base, BaseMin):
    __tablename__ = "cathashtag"
    catId = Column(Integer, ForeignKey("cat.id", ondelete="CASCADE"))
    hashtagId = Column(Integer, ForeignKey("hashtag.id"))

    __table_args__ = (Index("idx_catId_hashtagId", "catId"),)


class Post(BaseMin, Base):
    __tablename__ = "post"

    title = Column(String(50), nullable=False)
    uploaderId = Column(Integer, ForeignKey("user.id"))
    likeCount = Column(Integer, default=0)
    version = Column(Integer, default=0)

    __table_args__ = (Index("idx_uploader_id", "uploaderId"),)


class Image(BaseMin, Base):
    __tablename__ = "image"

    url = Column(String(255), nullable=False)
    postId = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))

    __table_args__ = (Index("idx_post_id", "postId"),)


class HashTag(BaseMin, Base):
    __tablename__ = "hashtag"

    hashtag = Column(String(50), nullable=False, unique=True)

    __table_args__ = (Index("idx_hashtag", "hashtag"),)


class Comment(BaseMin, Base):
    __tablename__ = "comment"

    comment = Column(String(255), nullable=False)
    nickname = Column(String(20), nullable=False)
    uploader = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"))
    postId = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"))


class Like(Base):
    __tablename__ = "like"

    ownerId = Column(Integer, ForeignKey("user.id", ondelete="CASCADE"), primary_key=True)
    postId = Column(Integer, ForeignKey("post.id", ondelete="CASCADE"), primary_key=True)


class RefreshToken(BaseMin, Base):
    __tablename__ = "refreshtoken"

    refresh_token = Column(String(255))
    userId = Column(Integer, ForeignKey("user.id"))


class CatFeature(Base):
    __tablename__ = "catfeature"

    cat_breed = Column(String(15), primary_key=True)
    feature = Column(String(255))


class Timeline(Base):
    __tablename__ = "timeline"

    userId = Column(Integer, ForeignKey("user.id"), primary_key=True)
    postId = Column(Integer, ForeignKey("post.id"), primary_key=True)


class TempUser(BaseMin, Base):
    __tablename__ = "tempuser"

    name = Column(String(10), nullable=False)
    nickname = Column(String(20), nullable=False, unique=True)
    email = Column(String(30), nullable=True, unique=True)
    password = Column(String(255), nullable=True)
    count = Column(Integer, nullable=False)
