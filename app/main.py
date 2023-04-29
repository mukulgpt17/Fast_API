from fastapi import FastAPI,Response,status,HTTPException,Depends
from fastapi.params import Body

from typing import Optional,List
from random import randrange 
import psycopg2 
from psycopg2.extras import RealDictCursor
import time 

from sqlalchemy.orm import Session
from database import engine,SessionLocal
import models,schemas

models.Base.metadata.create_all(bind=engine)
 
app= FastAPI()

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# to run the app in the termain head to app directory 
# run uvicorn main:app --reload (--reload is used if any changes are done it auto restarts the server )

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

@app.get("/posts",response_model=List[schemas.Post])
def get_posts(db:Session=Depends(get_db)):
    # RAW SQL Query
    # here we are connecting to the database for feteching all the daata 
    #fetchall return all the o/p from query while fetchone return just one o/p 
    # cursor.execute(""" SELECT * FROM posts""")
    # posts=cursor.fetchall()
    # return {"data" : posts} # return data in body of the response
    
    # using ORM (Sqlalchemy)
    posts=db.query(models.Post).all()
    return posts


@app.post("/posts",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db)): 

    # post:Post -> makes the post request have compulsion to follow the schema of POST class mentioned above 
    #note when creating a post the status code==201 

    # please note do not use f'strings in SQL query , it might cause the injection attack 
    # passing as parameter , library does santiation check before replacing %s with actual values. 

    # Raw SQL Query 
    # cursor.execute("""INSERT INTO posts(title,content,published) VALUES (%s , %s , %s) RETURNING *  """,(post.title,post.content,post.published))
    # post_data=cursor.fetchone()
    # # to push the the data to sql database in postgress we need to commit it 
    # conn.commit()
    # return {"post_detail":post_data} 

    # using ORM 
    # new_post=models.Post(title=post.title,content=post.content,published=post.published)
    # Wrinting title=post.title (imagine if we have 100s of col, it will very difficult to do this)
    
    new_post=models.Post(**post.dict())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@app.get("/posts/latest")
def get_latest_post():
    cursor.execute(""" SELECT * FROM "posts_Sql_alchemy" ORDER BY created_at DESC LIMIT 1 """ )
    post = cursor.fetchone()
    return post

@app.get("/posts/{id}",response_class=schemas.Post) #this is called {id} -> path parameter   
def get_single_post(id:int,db:Session=Depends(get_db)): 
    # make sure always mention like this id:int in argument 
    # id:int -> will make sure that it will convert string in to int 
    # if id is some string which cant be coverted to int then on frontend it will display correct error
    
    # RAW SQL 
    # cursor.execute("""SELECT * FROM posts WHERE id = %s   """,(str(id),))
    # # note passing value for %s -> make sure to convert the i/p value to string 
    # post=cursor.fetchone()
    # print(post)
    # # if post is not found then , I can(should) change the response status code to 404 
  
    # ORM 
    post=db.query(models.Post).filter(models.Post.id==id).first()   

    if not post:
         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"The post with id: {id} not found")
    return post


@app.delete("/posts/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db)):
    # if we delete something we need to change the status_code to 204 
    # Note : if status_code=204 then we should not send any data back 
    # delete posts 
    
    #Raw SQL 
    # cursor.execute(""" DELETE FROM posts WHERE id = %s  returning * """,(str(id),) )
    # delete_data=cursor.fetchone()
    # print(delete_data)
    # conn.commit()
    
    delete_data=db.query(models.Post).filter(models.Post.id==id)


    if delete_data.first() ==None: 
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="ID is not found")

    delete_data.delete(synchronize_session=False)
    db.commit()
    
    # Note : if status_code=204 then we should not send any data back 
    # return {"post_detail":"Post is deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@app.put("/posts/{id}")
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db)):
    
    # Raw SQL 
    # cursor.execute("""UPDATE posts SET title=%s , content=%s , published =%s  WHERE id = %s RETURNING * """,(post.title,post.content,post.published,str(id)))
    # post=cursor.fetchone()
    # conn.commit()
    # if post==None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id : {id} not found')
    # return {"data":post}

    # ORM
    post_query=db.query(models.Post).filter(models.Post.id==id)
    post_data=post_query.first()
  
    if post_data==None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'Post with id : {id} not found')
    
    post_query.update(post.dict(),synchronize_session=False)
    db.commit()

    return post

@app.post("/users",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    new_user=models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user
