import sys
# sys.path.append("..")
#fast api dependency 
from fastapi import Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from typing import List,Optional

# #postgress dependency 
# import psycopg2 
# from psycopg2.extras import RealDictCursor # this is used for getting columns name of the DB in postgress 

import time 

# orm (sqlalchemy)
from sqlalchemy.orm import Session
from sqlalchemy import func 

#database , models and schemas files 
from ..database import get_db
from .. import models,schemas,oauth2

#this creates a table in the DB if it doesn't exists

router=APIRouter(prefix="/posts",tags=['Posts'])
 

@router.get("/",response_model=List[schemas.postOut])
def get_posts(db:Session=Depends(get_db),user=Depends(oauth2.get_current_user),limit=500,skip=0,search:Optional[str]=""):
    # RAW SQL Query
    # here we are connecting to the database for feteching all the daata 
    #fetchall return all the o/p from query while fetchone return just one o/p 
    # cursor.execute(""" SELECT * FROM posts""")
    # posts=cursor.fetchall()
    # return {"data" : posts} # return data in body of the response
    
    # using ORM (Sqlalchemy)
    # print(user.email)
    posts=db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).all()
    post_count=db.query(models.Post,func.count(models.vote.post_id).label("votes")).join(models.vote,models.vote.post_id==models.Post.id, isouter=True).group_by(models.Post.id).all()
    return post_count

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.Post)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),user=Depends(oauth2.get_current_user)): 

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
    new_post=models.Post(owner_key=user.id,**post.dict()) # using **post.dict() -> makes it in the pattern key=value pair  
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post

@router.get("/{id}",response_model=schemas.Post) #this is called {id} -> path parameter   
def get_single_post(id:int,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)): 
    # make sure always mention like this id:int in argument 
    # id:int -> will make sure that it will convert string in to int 
    # if id is some string which cant be coverted to int then on frontend it will display respective error
    
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


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
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

    delete_post=delete_data.first()
    if delete_post.owner_key!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    delete_data.delete(synchronize_session=False)
    db.commit()
    # Note : if status_code=204 then we should not send any data back 
    # return {"post_detail":"Post is deleted"}
    return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.put("/{id}",response_model=schemas.Post)
def update_post(id:int,post:schemas.PostCreate,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
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
    
    if post_data.owner_key!=user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Not authorized to perform requested action")

    post_query.update(post.dict(),synchronize_session=False)
    db.commit()
    post_query_updated=db.query(models.Post).filter(models.Post.id==id).first()
    return post_query_updated