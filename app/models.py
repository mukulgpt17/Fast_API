from sqlalchemy import Boolean, Column, ForeignKey, Integer, String,TIMESTAMP, Text, text
from sqlalchemy.orm import relationship

from database import Base


class Post(Base) :
    __tablename__="posts_Sql_alchemy"
    id=Column(Integer,primary_key=True,index=True)
    title=Column(String,nullable=False)
    content=Column(String,nullable=False)
    published=Column(Boolean,server_default='TRUE',nullable=True)
    

class User(Base):
    __tablename__="users"
    id=Column(Integer,primary_key=True,index=True)
    email=Column(String,nullable=False,unique=True)
    password=Column(String,nullable=False)
    created_at=Column(TIMESTAMP(timezone=True),nullable=False,server_default=text('Now()'))