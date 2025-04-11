from pydantic import BaseModel, EmailStr, Field
from typing import Literal

class UserCreate(BaseModel):
    name: str
    email: str
    password: str | None = None
    phone: str | None = None
    bio: str | None = None
    image_url: str | None = None

class UserUpdate(BaseModel):
    name: str | None = None
    email: str | None = None
    password: str | None = None
    phone: str | None = None
    bio: str | None = None
    image_url: str | None = None

class LoginRequest(BaseModel):
    email: str | None = None
    password: str | None = None