from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from ..import schemas, crud
from ..database import get_db


router = APIRouter(
    tags=['users']
)


@router.post("/users/", response_model=schemas.UserResponse)
def create_user(user: schemas.UserCreate, status_code=status.HTTP_201_CREATED, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail=f'User with the email {user.email} already exists')
    return crud.create_user(db=db, user=user)


@router.get("/users/{id}", response_model=schemas.UserResponse)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    user = crud.get_user_by_id(db, user_id=user_id)
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User is the id {user_id} not found")
    return user


@router.get("/users/", response_model=list[schemas.UserResponse])
def get_users(db: Session = Depends(get_db)):
    users = crud.get_users(db)
    return users


@router.put("/users/{id}", response_model=schemas.UserResponse, status_code=status.HTTP_200_OK)
def update_user(user_id: int, user_info: schemas.UpdateUser, db: Session = Depends(get_db)):
    updated_user = crud.update_user(db=db, userinfo=user_info, user_id=user_id)

    return updated_user

# @router.get("/users/{user_email}", response_model=schemas.UserResponse)
# def get_user_by_email(user_email: str, db: Session = Depends(get_db)):
#     db_user = crud.get_user_by_email(db, email=user_email)
#     if db_user is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"User with email {user_email} does not exist")
#     return db_user
