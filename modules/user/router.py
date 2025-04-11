from fastapi import APIRouter, Depends, UploadFile, File, Form
from .utils.response import success_response, failure_response
from .schemas import UserCreate, UserUpdate
from .services import UserService

from sqlalchemy.orm import Session
from database import get_db
from typing import Union

router = APIRouter()

@router.get("/ping")
def ping():
    return {"message": "pong from user module"}

@router.post("/register")
async def register_user(
    name: str = Form(...),
    email: str = Form(...),
    password: str = Form(...),
    phone: str = Form(None),
    bio: str = Form(None),
    image_url: str = Form(None),
    image: Union[UploadFile, str, None] = File(None),
    db: Session = Depends(get_db)
):
    try:
        user_service = UserService(db)
        created_user = await user_service.register_user_with_image_or_url(
            name=name,
            email=email,
            password=password,
            phone=phone,
            bio=bio,
            image_url=image_url,
            image=image
        )
        return success_response(data={"user_id": created_user.id}, message="User registered successfully")
    except Exception as e:
        return failure_response(message=str(e))
    
@router.put("/user/update/{user_id}")
def update_user(
    user_id: int,
    name: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
    phone: str = Form(None),
    bio: str = Form(None),
    image_url: str = Form(None),
    image: UploadFile = File(None),
    db: Session = Depends(get_db)
):
    try:
        update_data = UserUpdate(
            name=name,
            email=email,
            password=password,
            phone=phone,
            bio=bio,
            image_url=image_url,
        )
        service = UserService(db)
        updated_user = service.update_user(user_id, update_data, image)
        return {"status": "success", "message": "User updated successfully", "data": {"user_id": updated_user.id}}
    except Exception as e:
        return {"status": "failure", "message": str(e), "data": None}

@router.get("/all-users")
def all_users(db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        users = user_service.get_all_users()
        return success_response(data=users, message="Users fetched successfully")
    except Exception as e:
        return failure_response(message=str(e))

@router.get("/details/{user_id}")
def get_user(user_id: int, db: Session = Depends(get_db)):
    try:
        user_service = UserService(db)
        user = user_service.get_user_by_id(user_id)
        if not user:
            return failure_response(message="User not found")
        return success_response(data=user, message="User details fetched successfully")
    except Exception as e:
        return failure_response(message=str(e))
