from sqlalchemy.orm import Session

from app import models
from app.schemas import schemas
class UserDao:
    _instance = None

    def __new__(cls):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance

    def get_user(self, db: Session, user_id: int):
        return db.query(models.User).filter(models.User.id == user_id).first()

    def get_user_by_email(self, db: Session, email: str):
        return db.query(models.User).filter(models.User.email == email).first()

    def get_users(self, db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.User).offset(skip).limit(limit).all()

    def create_user(self, db: Session, user: schemas.UserCreate):
        fake_hashed_password = user.password + "notreallyhashed"
        db_user = models.User(email=user.email, hashed_password=fake_hashed_password)
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user


