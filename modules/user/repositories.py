from sqlalchemy.orm import Session
from sqlalchemy import select
from passlib.hash import bcrypt
from . import schemas
from .models import User

class repository:
    def __init__(self, db: Session):
        self.db = db

    def create_user(self, user):
        db_user = User(
            name=user.get('name'),
            email=user.get('email'),
            hashed_password=user.get('hashed_password'),
            phone=user.get('phone'),
            bio=user.get('bio'),
            image_url=user.get('image_url')
        )
        self.db.add(db_user)
        self.db.commit()
        return db_user

    def get_all_users(self):
        return self.db.execute(select(User)).scalars().all()

    def get_user_by_id(self, user_id: int):
        query = select(User).where(User.id == user_id)
        return self.db.execute(query).scalar_one_or_none()
    
    def get_user_by_email(self, email: str):
        return self.db.query(User).filter(User.email == email).first()

    def update_user(self, user: User):
        self.db.commit()
        return user
