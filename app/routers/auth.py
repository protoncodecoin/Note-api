from fastapi import APIRouter, Depends, status, HTTPException, Response
from sqlalchemy.orm import Session

from .. import database, schemas, models, utils, oauth2

from fastapi.security.oauth2 import OAuth2PasswordRequestForm

router = APIRouter(
    tags=['Authentication']
)


# @router.post("/authenticate")
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(database.get_db)):
#     user = db.query(models.User).filter(
#         models.User.email == user_credentials.email).first()

#     if user == None:
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

#     # verify password
#     if not utils.verifypassword(user_credentials.password, user.password):
#         raise HTTPException(
#             status_code=status.HTTP_404_NOT_FOUND, detail=f'Invalid Credentials')

#     # create jwt token
#     access_token = oauth2.create_access_token(data={'user_id': user.id})

#     return {'access_token': access_token, 'token_type': 'bearer'}

# using auth2passwordrequestform


@router.post("/login", response_model=schemas.Token)
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(database.get_db)):
    user = db.query(models.User).filter(
        models.User.email == user_credentials.username).first()

    if user == None:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    # verify password
    if not utils.verifypassword(user_credentials.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail=f'Invalid Credentials')

    # create jwt token
    access_token = oauth2.create_access_token(data={'user_id': user.id})

    return {'access_token': access_token, 'token_type': 'bearer'}
