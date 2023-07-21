from sqlalchemy.orm import Session
from . import models, schemas

from fastapi import HTTPException, status

from .utils import hash_password

from passlib.context import CryptContext


pwd_context = CryptContext(schemes=['bcrypt'], deprecated='auto')


def get_note(db: Session, note_id: int):
    return db.query(models.Note).filter(models.Note.id == note_id).first()


def get_notes(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.Note).offset(skip).limit(limit).all()


def create_note(note: schemas.NoteCreate, user_id: int, db: Session):
    new_note = models.Note(
        title=note.title, content=note.content, owner_id=user_id)
    db.add(new_note)
    db.commit()
    db.refresh(new_note)

    return new_note


def delete_note(note_id: int, db: Session):
    db_note = db.query(models.Note).filter(models.Note.id == note_id)
    note = db_note.first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with the id of {id} is not found")
    db_note.delete()
    db.commit()


def update_note(note_id: int, note_update: schemas.NoteCreate, db: Session):
    query_note = db.query(models.Note).filter(models.Note.id == note_id)
    note = query_note.first()
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail='Note with the id of {note_id} does not exist')
    query_note.update(note_update.dict(), synchronize_session=False)
    db.commit()

    return query_note.first()


def get_users(db: Session, skip: int = 0, limit: int = 20):
    return db.query(models.User).offset(skip).limit(limit).all()


def get_user_by_email(db: Session, email: str):
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_id(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def create_user(db: Session, user: schemas.UserCreate):
    # hashed password
    hashed = hash_password(user.password)
    user.password = hashed
    new_user = models.User(name=user.name, age=user.age,
                           email=user.email, hashed_password=user.password)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return new_user


def update_user(db: Session, userinfo: schemas.UpdateUser, user_id: int):
    query_user = db.query(models.User).filter(models.User.id == user_id)
    user = query_user.first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"User with the id {user_id} is not found")
    query_user.update(userinfo.dict(), synchronize_session=False)
    db.commit()

    return query_user.first()
