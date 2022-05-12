from typing import Optional, List

from pydantic import BaseModel


class FileBase(BaseModel):
    name: str
    text: Optional[str] = ''


class FileCreate(FileBase):
    pass


class File(FileBase):
    id: str
    editor_id: int

    class Config:
        orm_mode = True

