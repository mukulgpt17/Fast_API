import sys
# sys.path.append("..")
from fastapi import FastAPI,Response,status,HTTPException,Depends,APIRouter

from sqlalchemy.orm import Session
from ..database import get_db
from .. import models,schemas,utils,oauth2

router=APIRouter(prefix="/users",tags=['Users'])

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserOut)
def create_user(user:schemas.UserCreate,db:Session=Depends(get_db)):
    user.password=utils.hash(user.password)
    new_user=models.User(**user.dict())
    # check if the user id not already registered.
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get("/{id}",response_model=schemas.UserOut)
def get_user(id:int , db: Session=Depends(get_db),user=Depends(oauth2.get_current_user)):
    user_db=db.query(models.User).filter(models.User.id==id).first()
    if not user_db:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f'User with {id} not found')
    return user_db