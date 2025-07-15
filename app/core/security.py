from fastapi import HTTPException, status, Depends
from passlib.context import CryptContext
import jwt
from datetime import datetime, timedelta, timezone
from database import get_session    
from typing import Annotated
from sqlmodel import Session, select
from models.user import User
from fastapi.security import OAuth2PasswordBearer

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SessionDep = Annotated[Session, Depends(get_session)]

SECRET_KEY = "This is my secret key"
ALGORITHM = "HS256"


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/user/login")

# Dependency to get the current authenticated user
async def get_current_user(token: Annotated[str, Depends(oauth2_scheme)], session: Session = Depends(get_session)):
    token_data = decode_access_token(token)
    username = token_data.get("username")
    user = get_user(username, session=session)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )
    return user

def hash_password(password: str) -> str:
    hashed_password = pwd_context.hash(password)
    return hashed_password

def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)

def get_user(username: str, session: SessionDep):
    user = session.exec(select(User).where(User.username == username)).first()
    return user

def generate_access_token(data: dict, expires_delta: int = None):
    if expires_delta:
        expires_delta = timedelta(minutes=expires_delta) 
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    data.update({"exp": expire})
    encoded_jwt = jwt.encode(data, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def decode_access_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials from token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        user_id: str = payload.get("id")
        if username is None:
            raise credentials_exception
        token_data = {"username": username, "id": user_id}
    except Exception as e:
        raise credentials_exception
    return token_data