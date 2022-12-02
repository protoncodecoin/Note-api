from fastapi import FastAPI, APIRouter, Depends, HTTPException, status, Response

from sqlalchemy.orm import Session

from .. import crud, schemas, crud, oauth2
from ..database import get_db


router = APIRouter(
    tags=['notes']
)


@router.post("/users/{user_id}/notes/", status_code=status.HTTP_201_CREATED, response_model=schemas.NoteResponse)
def create_note(user_id: int, note: schemas.NoteCreate, db: Session = Depends(get_db)):
    print(type(user_id))
    new_note = crud.create_note(db=db, note=note, user_id=user_id)
    return new_note


@router.get("/notes/", response_model=list[schemas.NoteResponse])
def get_notes(skip: int = 0, limit: int = 20, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    notes = crud.get_notes(db, skip=skip, limit=limit)
    return notes


@router.get("/notes/{id}", response_model=schemas.NoteResponse)
def get_note(id: int, db: Session = Depends(get_db)):
    note = crud.get_note(db, note_id=id)
    if note is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"Note with the id {id} not found")
    return note


# @router.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_note(id: int, db: Session = Depends(get_db)):
#     db_note = crud.get_note(db, note_id=id)
#     if db_note is None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail=f"Note with the id of {id} is not found")
#     db_note.delete()
#     db.commit()

@router.delete("/notes/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_note(id: int, db: Session = Depends(get_db)):
    db_note = crud.delete_note(note_id=id, db=db)

    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/notes/{id}", response_model=schemas.NoteResponse, status_code=status.HTTP_200_OK)
def update_note(note_id: int, note_update: schemas.NoteCreate, db: Session = Depends(get_db)):
    db_note = crud.update_note(db=db, note_id=note_id, note_update=note_update)

    return db_note
