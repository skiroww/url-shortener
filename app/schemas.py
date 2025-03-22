from datetime import datetime
from typing import Optional
from pydantic import BaseModel, EmailStr, HttpUrl, constr


class UserBase(BaseModel):
    username: str
    email: EmailStr


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: str
    created_at: datetime

    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str


class LoginData(BaseModel):
    username: str
    password: str


class LinkBase(BaseModel):
    original_url: HttpUrl
    custom_alias: Optional[constr(min_length=3, max_length=50, pattern=r"^[a-zA-Z0-9_-]+$")] = None
    expires_at: Optional[datetime] = None


class LinkCreate(LinkBase):
    pass


class LinkUpdate(BaseModel):
    original_url: Optional[HttpUrl] = None
    custom_alias: Optional[str] = None
    expires_at: Optional[datetime] = None


class LinkPreview(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    image_url: Optional[str] = None


class LinkInfo(LinkBase):
    id: str
    short_code: str
    user_id: str
    created_at: datetime
    click_count: int
    last_accessed: Optional[datetime]
    preview: Optional[LinkPreview] = None

    class Config:
        from_attributes = True