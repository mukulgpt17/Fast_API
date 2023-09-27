from fastapi import APIRouter, Depends , status , HTTPException,Response 
from sqlalchemy.orm import Session 
from typing_extensions import Annotated

#database , models and schemas files 
from ..database import get_db
from .. import models,schemas,utils,oauth2

#token and security 
from fastapi.security import OAuth2PasswordRequestForm

router= APIRouter(prefix='/auth', tags=["Authentication"])

@router.post('/login')
def login(user_credentials :OAuth2PasswordRequestForm=Depends() , db: Session=Depends(get_db)): 
    user = db.query(models.User).filter(models.User.email==user_credentials.username).first()
    
    if not user: 
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User not defined")
    
    if not utils.verify(user_credentials.password,user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"User not defined")

    access_token = oauth2.create_access_token(data={'user_id' : user.id })
    # return access_token
    token=schemas.Token(access_token=access_token,token_type='bearer')
    return token    