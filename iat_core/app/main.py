from typing import Union
from fastapi import FastAPI, Request, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from database.details import SessionLocal, engine, Base
import os
import time
import dotenv

dotenv.load_dotenv('../.env')

from app import models
from app.dao import user_dao
from app.schemas import schemas

# This will create the tables in the database
Base.metadata.create_all(bind=engine)

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
@app.get("/api/health")
def read_root(request: Request):
    return {"Message": "Hello World",
            "ip": request.client.host}

@app.get("/api/delay")
def delay_call(request: Request):
    time.sleep(10)
    return read_root(request=request)

@app.get("/api/secret")
def read_secret(secret: str):
    return {"secret": os.getenv(secret)}


@app.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    
    db_user = user_dao.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_dao.create_user(db=db, user=user)

@app.get("/users/", response_model=list[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = user_dao.get_users(db, skip=skip, limit=limit)
    return users