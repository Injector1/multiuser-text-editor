from typing import Optional, List

from pydantic import BaseModel


class FileBase(BaseModel):
    name: str
    text: Optional[str] = ''


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: int
    editor_id: int

    class Config:
        orm_mode = True


class UserBase(BaseModel):
    id: str


class UserCreate(UserBase):
    pass


class User(UserBase):
    id: int
    is_active: bool
    files: List[File] = []

    class Config:
        orm_mode = True
