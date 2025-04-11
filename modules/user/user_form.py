# user_form_schema.py
from fastapi import Form, File, UploadFile
from typing import Optional

class UserRegisterForm:
    def __init__(
        self,
        name: str = Form(...),
        email: str = Form(...),
        password: str = Form(...),
        phone: Optional[str] = Form(None),
        bio: Optional[str] = Form(None),
        image_url: Optional[str] = Form(None),
        image: Optional[UploadFile] = File(None),
    ):
        self.name = name
        self.email = email
        self.password = password
        self.phone = phone
        self.bio = bio
        self.image_url = image_url
        self.image = image if image and image.filename else None
