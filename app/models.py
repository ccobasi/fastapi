from tokenize import String
from turtle import title
from xmlrpc.client import Boolean
from markupsafe import string
from sqlalchemy import Column, Integer
from .database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, nullable=False)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    published = Column(Boolean, default=True)
