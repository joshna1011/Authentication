import os
import shutil

from sqlalchemy.orm import Session
from ..repositories import Repository
from ..schemas import UserUpdate
from passlib.hash import bcrypt
from uuid import uuid4
from fastapi import UploadFile
from sqlalchemy.orm import Session
from typing import Optional, Union

class UserService:
    def __init__(self, db: Session):
        self.repo = Repository(db)
    
    async def register_user_with_image_or_url(
        self,
        name: str,
        email: str,
        password: str,
        phone: Optional[str],
        bio: Optional[str],
        image_url: Optional[str],
        image: Optional[UploadFile]
    ):
        final_image_url = None

        if image and image.filename == "":
            image = None

        # Save image if uploaded
        if image:
            ext = image.filename.split('.')[-1]
            filename = f"{uuid4().hex}.{ext}"
            os.makedirs("media", exist_ok=True)
            file_path = os.path.join("media", filename)

            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)

            final_image_url = f"/media/{filename}"
        
        elif image_url:
            final_image_url = image_url

        hashed_password = bcrypt.hash(password)
        user_data = {
            "name": name,
            "email": email,
            "hashed_password": hashed_password,
            "phone": phone,
            "bio": bio,
            "image_url": final_image_url
        }
        return self.repo.create_user(user_data)

    def get_all_users(self):
        users = self.repo.get_all_users()
        users = [{"user_id": user.id, "name": user.name, "email": user.email, "phone": user.phone, "bio": user.bio, "image_url": user.image_url} for user in users]
        return users

    def get_user_by_id(self, user_id: int):
        user = self.repo.get_user_by_id(user_id)
        if user:
            return {"user_id": user.id, "name": user.name, "email": user.email, "phone": user.phone, "bio": user.bio, "image_url": user.image_url}
        return user
    
    def update_user(self, user_id: int, update_data: UserUpdate, image: UploadFile = None):
        user = self.repo.get_user_by_id(user_id)
        if not user:
            raise Exception("User not found")

        # Check if email already exists for a different user
        if update_data.email:
            existing_user = self.repo.get_user_by_email(update_data.email)
            if existing_user and existing_user.id != user_id:
                raise Exception("Email already in use")

        update_dict = update_data.model_dump(exclude_unset=True)

        if "password" in update_dict:
            update_dict["hashed_password"] = bcrypt.hash(update_dict.pop("password"))

        # Handle image upload
        if image:
            ext = image.filename.split('.')[-1]
            filename = f"{uuid4().hex}.{ext}"
            os.makedirs("media", exist_ok=True)
            file_path = os.path.join("media", filename)
            with open(file_path, "wb") as buffer:
                shutil.copyfileobj(image.file, buffer)
            update_dict["image_url"] = f"/media/{filename}"

        # Apply all updates
        for key, value in update_dict.items():
            setattr(user, key, value)

        self.repo.update_user(user)
        return user
