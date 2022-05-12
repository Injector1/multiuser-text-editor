from database import Base

from sqlalchemy import Column, String


class File(Base):
    __tablename__ = "files"

    id = Column(String, primary_key=True, index=True)
    name = Column(String, unique=True)
    text = Column(String)

