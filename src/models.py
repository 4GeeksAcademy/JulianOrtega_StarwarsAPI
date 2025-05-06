from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import String, Integer, Enum, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship
from typing import List

db = SQLAlchemy()

class User(db.Model):
    __tablename__ = 'User'

    id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)
    firstname: Mapped[str] = mapped_column(String(120), nullable=False)
    lastname: Mapped[str] = mapped_column(String(120), nullable=False)
    email: Mapped[str] = mapped_column(String(120), nullable=False, unique=True)

    posts: Mapped[List["Post"]] = relationship(back_populates="author")
    comments: Mapped[List["Comment"]] = relationship(back_populates="author")
    followers: Mapped[List["Follower"]] = relationship(
        foreign_keys="[Follower.user_to_id]", back_populates="followed"
    )
    following: Mapped[List["Follower"]] = relationship(
        foreign_keys="[Follower.user_from_id]", back_populates="follower"
    )

    def serialize(self):
        return {
            "id": self.id,
            "username": self.username,
            "firstname": self.firstname,
            "lastname": self.lastname,
            "email": self.email,
        }

class Follower(db.Model):
    __tablename__ = 'Follower'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_from_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    user_to_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)

    follower: Mapped["User"] = relationship(
        back_populates="following", foreign_keys=[user_from_id]
    )
    followed: Mapped["User"] = relationship(
        back_populates="followers", foreign_keys=[user_to_id]
    )

    def serialize(self):
        return {
            "id": self.id,
            "user_from_id": self.user_from_id,
            "user_to_id": self.user_to_id,
        }

class Post(db.Model):
    __tablename__ = 'Post'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)

    author: Mapped["User"] = relationship(back_populates="posts")
    comments: Mapped[List["Comment"]] = relationship(back_populates="post")
    media: Mapped[List["Media"]] = relationship(back_populates="post")

    def serialize(self):
        return {
            "id": self.id,
            "user_id": self.user_id,
        }

class Comment(db.Model):
    __tablename__ = 'Comment'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    commenttext: Mapped[str] = mapped_column(String(200), nullable=True)
    User_id: Mapped[int] = mapped_column(ForeignKey('User.id'), nullable=False)
    Post_id: Mapped[int] = mapped_column(ForeignKey('Post.id'), nullable=False)

    author: Mapped["User"] = relationship(back_populates="comments")
    post: Mapped["Post"] = relationship(back_populates="comments")

    def serialize(self):
        return {
            "id": self.id,
            "commenttext": self.commenttext,
            "User_id": self.User_id,
            "Post_id": self.Post_id,
        }

class Media(db.Model):
    __tablename__ = 'Media'

    id: Mapped[int] = mapped_column(primary_key=True, autoincrement=True)
    type: Mapped[str] = mapped_column(Enum('1', '2', '3', name='media_type'), nullable=False)
    url: Mapped[str] = mapped_column(String(120), nullable=True)
    Post_id: Mapped[int] = mapped_column(ForeignKey('Post.id'), nullable=False)

    post: Mapped["Post"] = relationship(back_populates="media")

    def serialize(self):
        return {
            "id": self.id,
            "type": self.type,
            "url": self.url,
            "Post_id": self.Post_id,
        }