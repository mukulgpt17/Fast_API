from fastapi import Response,status,HTTPException,Depends,APIRouter
from fastapi.params import Body
from typing import List,Optional
from sqlalchemy import and_
from ..database import get_db
from .. import models,schemas,utils,oauth2
from sqlalchemy.orm import Session
router=APIRouter(prefix="/vote",tags=['Vote'])

@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote ,db:Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
    # if vote.dir==1 then like 
    if vote.dir==1 : 
        #check if post exist 
        #check if already liked then dont do anything 
        # add the data to db 
        post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
        if not post : 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail =f"Post with Id {vote.post_id} not found")
        check_vote=db.query(models.vote).filter(and_(models.vote.post_id==vote.post_id, models.vote.user_id==user.id)).first()
        if check_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"This post is already liked")
        
        vote_post=models.vote(user_id=user.id,post_id=vote.post_id)
        db.add(vote_post)
        db.commit()
        db.refresh(vote_post)
        return "Post has been liked"
    elif vote.dir==0: 
        # check if post exist 
        post=db.query(models.Post).filter(models.Post.id==vote.post_id).first()
        if not post : 
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail =f"Post with Id {vote.post_id} not found")
        check_vote=db.query(models.vote).filter(and_(models.vote.post_id==vote.post_id, models.vote.user_id==user.id)).first()
        if not check_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"This post is not liked")

        vote_query=db.query(models.vote).filter(and_(models.vote.post_id==vote.post_id, models.vote.user_id==user.id))
        vote_query.delete(synchronize_session=False)
        db.commit()
        #check if post is liked 
        #remove from db 
        # if vote.dir==0 then unlike 
        return "post is unliked"    

