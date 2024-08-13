from sqlalchemy.orm import Session

from app import models

from app.schemas import schemas

class ItemsDAO:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_items(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Item).offset(skip).limit(limit).all()

    def create_user_item(self, db: Session, item: schemas.ItemCreate, user_id: int):
        db_item = models.Item(**item.model_dump(), owner_id=user_id)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        return db_item

