from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange 
import psycopg2 



app= FastAPI()

class Post(BaseModel):
    # current are mandatory fields in the schema 
    title:str
    content:str
    published:bool =True # will have true if not passed 
    # below are optinal fields in the schema 
    
    # note : below we have imported Optional library 
    rating: Optional[int]=None


def find_post(id):
    for pt in my_posts:
        if pt["id"]==id:
            return pt

def find_index_post(id):
    for idx,pt in enumerate(my_posts):
        if pt["id"]==id:
            return idx 

@app.get("/")
async def root():
    return {"message": "Welcome to main Page"}

# @app.post("/post_new")
# def create_posts(payload : dict =Body(...)):
#     print(payload)
#     return {"message_new_post":f"title {payload['title']}"}  

@app.get("/posts")
def get_posts():
    return {"data" : my_posts} # return data in body of the response 

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post): # post:Post -> makes the post request have compulsion to follow the schema of POST class mentioned above 
    #note when creating a post the status code==201 
    post_dict=post.dict()
    post_dict["id"]=randrange(1,10000000)
    my_posts.append(post_dict)
    return {"post_detail":post_dict} 

@app.get("/posts/latest")
def get_latest_post():
    post=my_posts[-1]
    return {"post_detail" :post}

# @app.get("/posts/{id}")
# def get_single_post(id:int,response: Response): 
#     # make sure always mention like this id:int in argument 
#     # id:int -> will make sure that it will convert string ip to int 
#     # if id is some string which cant be coverted to int then on frontend it will display correct error
#     post=find_post(int(id))
#     # if post is not found then , I can(should) change the response status code to 404 
#     if not post:
#         # response.status_code=404  -> here we hard coded the satus 
#         response.status_code=status.HTTP_404_NOT_FOUND
#         return {f"The post with id: {id} not found"}
#     return {"post_detail":post}

# better and clean way to deal with HTTP exception 

@app.get("/posts/{id}") #this is called {id} -> path parameter   
def get_single_post(id:int): 
    # make sure always mention like this id:int in argument 
    # id:int -> will make sure that it will convert string ip to int 
    # if id is some string which cant be coverted to int then on frontend it will display correct error
    post=find_post(id)
    # if post is not found then , I can(should) change the response status code to 404 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id: {id} not found")
    return {"post_detail":post}

@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # if we delete something we need to change the status_code to 204 
    # Note : if status_code=204 then we should not send any data back 
    # delete posts 
    # find the index and delete it 
    index=find_index_post(id)
    if index ==None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID is not found")

    my_posts.pop(index)
    # Note : if status_code=204 then we should not send any data back 
    # return {"post_detail":"Post is deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    idx=find_index_post(id)
    if idx==None :
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id: {id} not found")

    post_dict=post.dict()
    post_dict['id']=id
    my_posts[idx]=post_dict
    return {"data":post_dict}
 