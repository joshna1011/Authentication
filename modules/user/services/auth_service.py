from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from fastapi import HTTPException, status
from ..models import User
from ..repositories import Repository
from ..schemas import LoginRequest
from dotenv import load_dotenv 
from google.oauth2 import id_token
from google.auth.transport import requests
import os
import requests as httpx

load_dotenv()

class AuthService:
    def __init__(self, db: Session):
        self.db = db
        self.repo = Repository(db)

    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        return bcrypt.verify(plain_password, hashed_password)

    def login(self, data: LoginRequest) -> User:
        email = data.email
        password = data.password
        user = self.repo.get_user_by_email(email)
        if not user or not self.verify_password(password, user.hashed_password):
            raise HTTPException(status_code=401, detail="Invalid email or password")
        return user

    def verify_google_token(self, code: str) -> str:
        google_client_id = os.getenv("GOOGLE_CLIENT_ID")
        google_client_secret = os.getenv("GOOGLE_CLIENT_SECRET")
        google_redirect_uri = os.getenv("GOOGLE_REDIRECT_URI")
        token_url = "https://oauth2.googleapis.com/token"

        data = {
            "code": code,
            "client_id": google_client_id,
            "client_secret": google_client_secret,
            "redirect_uri": google_redirect_uri,
            "grant_type": "authorization_code",
        }

        # Exchange code for tokens
        response = httpx.post(token_url, data=data)
        if response.status_code != 200:
            raise HTTPException(status_code=401, detail="Failed to exchange code for tokens")

        tokens = response.json()
        id_token_str = tokens.get("id_token")

        if not id_token_str:
            raise HTTPException(status_code=401, detail="ID token not found")

        # Verify ID token
        try:
            idinfo = id_token.verify_oauth2_token(id_token_str, requests.Request(), google_client_id)
            email = idinfo.get("email")
            if not email:
                raise ValueError("Email not found in token")
            name = idinfo.get("name")
            picture = idinfo.get("picture")
            self.repo.get_user_by_email(email)  # Check if user exists
            if not self.repo.get_user_by_email(email):
                self.repo.create_user({"name": name, "email": email, "image_url": picture})  # Create user if not exists
            return email
        except ValueError as e:
            raise HTTPException(status_code=401, detail=f"Invalid Google token: {str(e)}")
        
    def verify_facebook_token(self, code: str):
        facebook_client_id = os.getenv("FACEBOOK_CLIENT_ID")
        facebook_client_secret = os.getenv("FACEBOOK_CLIENT_SECRET")
        facebook_redirect_uri = os.getenv("FACEBOOK_REDIRECT_URI")
        token_url = "https://graph.facebook.com/v18.0/oauth/access_token"
        params = {
            "client_id": facebook_client_id,
            "redirect_uri": facebook_redirect_uri,
            "client_secret": facebook_client_secret,
            "code": code,
        }

        token_response = requests.get(token_url, params=params)
        if token_response.status_code != 200:
            raise HTTPException(status_code=401, detail="Invalid Facebook code")

        access_token = token_response.json().get("access_token")

        user_info_url = "https://graph.facebook.com/me"
        user_params = {
            "fields": "id,name,email",
            "access_token": access_token
        }

        user_info = requests.get(user_info_url, params=user_params).json()
        email = user_info.get("email")
        if not email:
            raise HTTPException(status_code=400, detail="Email not found in Facebook response")

        # Now login or register the user
        user = self.repo.get_user_by_email(email)
        name = user_info.get("name")
        if not user:
            self.repo.create_user({"name": name, "email": email})  # Create user if not exists
        return user
