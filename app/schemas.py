from datetime import datetime
from pydantic import BaseModel,EmailStr


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



#this class is created for modelling the response we send after created a post req 
class Post(PostBase):
    id:int
    created_at:datetime
    #class Congif is crated as when using ORM to insert data to DB , it returns and ORM model value not a dict
    #pydyantic model only works on dict type and hence this part of the code helps to convert ORM model type to dict
    class Config :
        orm_mode=True

class UserCreate(BaseModel):
    email:EmailStr
    password:str

class UserOut(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config :
        orm_mode=True