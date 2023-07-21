from datetime import datetime
from pydantic import BaseModel, EmailStr
from typing import Optional


class NoteBase(BaseModel):
    title: str
    content: str


class NoteCreate(NoteBase):
    pass


class NoteResponse(NoteBase):
    id: int
    owner_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    email: str
    name: str
    age: int


class UserCreate(UserBase):
    password: str


class UserResponse(UserBase):
    id: int
    is_active: bool
    notes: list[NoteResponse] = []

    class Config:
        orm_mode = True


class UpdateUser(BaseModel):
    email: str
    name: str


class UserLogin(BaseModel):
    email: str
    password: str


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    id: Optional[str]
