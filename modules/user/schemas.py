from pydantic import BaseModel

class UserCreate(BaseModel):
    name: str
    email: str
    password: str
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

class UserOut(BaseModel):
    id: int
    name: str
    email: str

    class Config:
        orm_mode = True