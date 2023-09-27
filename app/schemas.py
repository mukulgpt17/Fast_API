from datetime import datetime
from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class PostBase(BaseModel):
    #Base Model is used for schema creation
    # current are mandatory fields in the schema 
    title:str
    content:str
    published:bool =True # will have true if not passed 

    # below are optinal fields in the schema    
    # note : below we have imported Optional library 
    # rating: Optional[int]=None

class PostCreate(PostBase):
    pass

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config :
        orm_mode=True

#this class is created for modelling the response we send after created a post req 
class Post(PostBase):
    id:int
    created_at:datetime
    owner_key:int
    users : UserOut 
    #class Congif is crated as when using ORM to insert data to DB , it returns and ORM model value not a dict
    #pydyantic model only works on dict type and hence this part of the code helps to convert ORM model type to dict
    class Config :
        orm_mode=True

class postOut(BaseModel):
    Post:Post
    votes:int
    class Config: 
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserLogin(BaseModel): 
    email : EmailStr
    password : str

class Token(BaseModel):
    access_token:str
    token_type:str

class TokenData(BaseModel):
    id:Optional[str]

class Vote(BaseModel):
    post_id:int 
    dir:int =Field(ge=-1,le=1)
