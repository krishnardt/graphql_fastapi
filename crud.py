from models import Users
from sqlalchemy.orm import Session

import models, schemas
import json
from database import SessionLocal, engine

models.Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()




def get_user(db: Session, user_name: str):
    return db.query(models.Users).filter(models.Users.name == user_name)


def get_user_by_email(db: Session, email: str):
    return db.query(models.Users).filter(models.Users.email == email).first()


def get_users( skip: int = 0, limit: int = 100):
	with SessionLocal() as db:
		users_data = db.query(models.Users).offset(skip).limit(limit).all()
		#print(users_data)
		temp_data = [user.__dict__ for user in users_data]
		#print(temp_data)
	return temp_data


def create_user(db: Session, user: schemas.NewUser):
    secret_password = user.password + "notreallyhashed"
    db_user = models.Users(name=user.name, email=user.email, password=secret_password)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user




