from fastapi import FastAPI,Response,status,HTTPException
from fastapi.params import Body
from pydantic import BaseModel
from typing import Optional
from random import randrange 
import psycopg2 
from psycopg2.extras import RealDictCursor
import time 

app= FastAPI()

# to run the app in the termain head to app directory 
# run uvicorn main:app --reload (--reload is used if any changes are done it auto restarts the server )

class Post(BaseModel):
    #Base Model is used for schema creation
    # current are mandatory fields in the schema 
    title:str
    content:str
    published:bool =True # will have true if not passed 
    # below are optinal fields in the schema 
    
    # note : below we have imported Optional library 
    rating: Optional[int]=None

while True:
    try : 
        conn=psycopg2.connect(host='localhost',database='fastapi',user ='postgres'
                            ,password='Muk@2317',cursor_factory=RealDictCursor )
        cursor=conn.cursor()
        print("Database connection was succesfull")
        break
    except Exception as err:
        print("Connecting to database failed")
        print("error",err)
        time.sleep(2)

@app.get("/")
async def root():
    return {"message": "Welcome to main Page"}

@app.get("/posts")
def get_posts():
    # here we are connecting to the database for feteching all the daata 
    #fetchall return all the o/p from query while fetchone return just one o/p 
    cursor.execute(""" SELECT * FROM posts""")
    posts=cursor.fetchall()
    return {"data" : posts} # return data in body of the response 

@app.post("/posts",status_code=status.HTTP_201_CREATED)
def create_posts(post: Post): 
    # post:Post -> makes the post request have compulsion to follow the schema of POST class mentioned above 
    #note when creating a post the status code==201 

    # please note do not use f'strings in SQL query , it might cause the injection attack 
    # passing as parameter , library does santiation check before replacing %s with actual values. 

    cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s , %s , %s) RETURNING *  """,(post.title,post.content,post.published))
    post_data=cursor.fetchone()
    # to push the the data to sql database in postgress we need to commit it 
    conn.commit()
    return {"post_detail":post_data} 


@app.get("/posts/latest")
def get_latest_post():
    
    cursor.execute(""" SELECT * FROM posts ORDER BY created_at DESC LIMIT 1 """ )
    post = cursor.fetchone()
    return {"post_detail" :post}

@app.get("/posts/{id}") #this is called {id} -> path parameter   
def get_single_post(id:int): 
    # make sure always mention like this id:int in argument 
    # id:int -> will make sure that it will convert string in to int 
    # if id is some string which cant be coverted to int then on frontend it will display correct error
    cursor.execute("""SELECT * FROM posts WHERE id = %s   """,(str(id),))
    # note passing value for %s -> make sure to convert the i/p value to string 
    post=cursor.fetchone()
    print(post)
    # if post is not found then , I can(should) change the response status code to 404 
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id: {id} not found")
    return {"post_detail":post}


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int):
    # if we delete something we need to change the status_code to 204 
    # Note : if status_code=204 then we should not send any data back 
    # delete posts 
 
    cursor.execute(""" DELETE FROM posts WHERE id = %s  returning * """,(str(id),) )
    delete_data=cursor.fetchone()
    print(delete_data)
    conn.commit()

    if delete_data ==None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID is not found")

    # Note : if status_code=204 then we should not send any data back 
    # return {"post_detail":"Post is deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:Post):
    
    cursor.execute("""UPDATE posts SET title=%s , content=%s , published =%s  WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    post=cursor.fetchone()
    conn.commit()
    if post==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id : {id} not found')
    return {"data":post}
 