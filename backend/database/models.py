from database import Base

from sqlalchemy import Boolean, Column, ForeignKey, Integer, String
from sqlalchemy.orm import relationship


class File(Base):
    __tablename__ = "files"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)
    text = Column(String)
    editor_id = Column(String, ForeignKey("users.id"))

    editor = relationship("User", back_populates="files")


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    files = relationship("File", back_populates="editor")
