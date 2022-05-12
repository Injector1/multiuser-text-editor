import uuid

from sqlalchemy.orm import Session

from . import models, schemas


def get_user(db: Session, user_id: int):
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_users(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.User).offset(skip).limit(limit).all()


def create_user(db: Session):
    user_id = str(uuid.uuid1())
    db_user = models.User(id=user_id)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_items(db: Session, skip: int = 0, limit: int = 100):
    return db.query(models.File).offset(skip).limit(limit).all()


def get_file_by_id(db: Session, file_id: str):
    return db.query(models.File).filter(models.File.id == file_id).first()


def create_user_file(db: Session, item: schemas.FileCreate, user_id: int):
    db_item = models.File(**item.dict(), editor_id=user_id)
    db.add(db_item)
    db.commit()
    db.refresh(db_item)
    return db_item
