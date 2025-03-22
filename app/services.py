import uuid
import random
import string
from datetime import datetime, timedelta
from typing import Optional
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from fastapi import HTTPException, Depends
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from passlib.context import CryptContext
from .models import User, Link
from .schemas import UserCreate, LinkCreate, LinkUpdate, LinkInfo
from .config import settings
from .link_validator import LinkValidator
from .database import get_db

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


class AuthService:
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password: str) -> str:
        return pwd_context.hash(password)

    @staticmethod
    def create_user(db: Session, user: UserCreate) -> User:
        db_user = User(
            id=str(uuid.uuid4()),
            username=user.username,
            email=user.email,
            password=AuthService.get_password_hash(user.password)
        )
        try:
            db.add(db_user)
            db.commit()
            db.refresh(db_user)
            return db_user
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Username or email already registered")

    @staticmethod
    def authenticate_user(db: Session, username: str, password: str) -> Optional[User]:
        user = db.query(User).filter(User.username == username).first()
        if not user or not AuthService.verify_password(password, user.password):
            return None
        return user

    @staticmethod
    def create_access_token(data: dict) -> str:
        to_encode = data.copy()
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        return encoded_jwt

    @staticmethod
    async def get_current_user(db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)) -> User:
        credentials_exception = HTTPException(
            status_code=401,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            user_id: str = payload.get("sub")
            if user_id is None:
                raise credentials_exception
        except JWTError:
            raise credentials_exception

        user = db.query(User).filter(User.id == user_id).first()
        if user is None:
            raise credentials_exception
        return user


class LinkService:
    @staticmethod
    def generate_short_code(length: int = 6) -> str:
        chars = string.ascii_letters + string.digits
        return ''.join(random.choice(chars) for _ in range(length))

    @staticmethod
    def create_link(db: Session, link_data: LinkCreate, user: Optional[User] = None) -> Link:
        validator = LinkValidator()
        url_str = str(link_data.original_url)
        if not validator.validate_url(url_str):
            raise HTTPException(status_code=400, detail="Invalid URL format")
        validator.is_safe_url(url_str)

        if link_data.custom_alias:
            validator.validate_alias(link_data.custom_alias)

        preview = validator.generate_preview(url_str)

        db_link = Link(
            id=str(uuid.uuid4()),
            original_url=url_str,
            short_code=link_data.custom_alias or LinkService.generate_short_code(),
            custom_alias=link_data.custom_alias,
            user_id=user.id if user else None,
            expires_at=link_data.expires_at,
            preview=preview
        )

        try:
            db.add(db_link)
            db.commit()
            db.refresh(db_link)
            return db_link
        except IntegrityError:
            db.rollback()
            raise HTTPException(status_code=400, detail="Short code or custom alias already exists")

    @staticmethod
    def get_link(db: Session, short_code: str) -> Link:
        link = db.query(Link).filter(Link.short_code == short_code).first()
        if not link:
            raise HTTPException(status_code=404, detail="Link not found")
        
        if link.expires_at and link.expires_at < datetime.utcnow():
            raise HTTPException(status_code=410, detail="Link has expired")
        
        return link

    @staticmethod
    def update_link(db: Session, short_code: str, link_data: LinkUpdate, user: User) -> Link:
        link = LinkService.get_link(db, short_code)
        
        if link.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to update this link")

        if link_data.original_url:
            validator = LinkValidator()
            url_str = str(link_data.original_url)
            validator.validate_url(url_str)
            validator.is_safe_url(url_str)
            link.original_url = url_str
            link.preview = validator.generate_preview(url_str)

        if link_data.expires_at:
            link.expires_at = link_data.expires_at

        db.commit()
        db.refresh(link)
        return link

    @staticmethod
    def delete_link(db: Session, short_code: str, user: User) -> None:
        link = LinkService.get_link(db, short_code)
        
        if link.user_id != user.id:
            raise HTTPException(status_code=403, detail="Not authorized to delete this link")

        db.delete(link)
        db.commit()

    @staticmethod
    def increment_click_count(db: Session, link: Link) -> None:
        link.click_count += 1
        link.last_accessed = datetime.utcnow()
        db.commit()

    @staticmethod
    def search_by_url(db: Session, original_url: str) -> Optional[Link]:
        return db.query(Link).filter(Link.original_url == original_url).first() 