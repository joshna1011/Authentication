from fastapi import APIRouter, Depends, UploadFile, File, Form, HTTPException
from fastapi.responses import RedirectResponse
from .utils.response import success_response, failure_response
from .schemas import UserCreate, UserUpdate, LoginRequest
from .services import UserService, AuthService

from sqlalchemy.orm import Session
from database import get_db
from typing import Union
import os
import urllib.parse

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
    
@router.put("/update/{user_id}")
def update_user(
    user_id: int,
    name: str = Form(None),
    email: str = Form(None),
    password: str = Form(None),
    phone: str = Form(None),
    bio: str = Form(None),
    image_url: str = Form(None),
    image: Union[UploadFile, str, None] = File(None),
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

@router.post("/login/email")
def login(data: LoginRequest, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        return auth_service.login_with_email(data)
    except Exception as e:
        return failure_response(message=str(e))
  
@router.get("/login/google")
def login_with_google():
    try:
        base_url = "https://accounts.google.com/o/oauth2/v2/auth"
        params = {
            "client_id": os.getenv("GOOGLE_CLIENT_ID"),
            "redirect_uri": os.getenv("GOOGLE_REDIRECT_URI"),
            "response_type": "code",
            "scope": "openid email profile",
            "access_type": "offline",
            "prompt": "consent"
        }
        url = f"{base_url}?{urllib.parse.urlencode(params)}"
        return RedirectResponse(url)
    except Exception as e:
        return failure_response(message=str(e))

@router.get("/auth/google/callback")
def google_callback(code: str, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        data = auth_service.verify_google_token(code)
        return success_response(data=data, message="Google callback received")
    except Exception as e:
        return failure_response(message=str(e))

@router.get("/login/facebook")
def login_with_facebook():
    try:
        fb_auth_url = "https://www.facebook.com/v18.0/dialog/oauth"
        params = {
            "client_id": os.getenv("FACEBOOK_CLIENT_ID"),
            "redirect_uri": os.getenv("FACEBOOK_REDIRECT_URI"),
            "response_type": "code",
            "scope": "email",
        }
        url = f"{fb_auth_url}?{urllib.parse.urlencode(params)}"
        return RedirectResponse(url)
    except Exception as e:
        return failure_response(message=str(e))

@router.get("/auth/facebook/callback")
def facebook_callback(code: str, db: Session = Depends(get_db)):
    try:
        auth_service = AuthService(db)
        data = auth_service.verify_facebook_token(code)
        return success_response(data=data, message="Facebook callback received")
    except Exception as e:
        return failure_response(message=str(e))

@router.post("/logout")
def logout():
    # Frontend should just delete the token
    return success_response(data={}, message="Successfully logged out")
