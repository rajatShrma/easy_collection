from models.user import User
from schemas.user import CreateUser, ReadUser, LoginUser
from database import get_session    
from typing import Annotated
from sqlmodel import Session, select
from fastapi import APIRouter, Depends, HTTPException, status
from core.security import generate_access_token, hash_password, verify_password, get_current_user

router = APIRouter(prefix="/user", tags=["User"])
SessionDep = Annotated[Session, Depends(get_session)]


@router.post("/register", response_model=ReadUser)   # user/register
def create_user(user_data: CreateUser, session: SessionDep):
    user_context  = User(
        first_name = user_data.first_name,
        last_name = user_data.last_name,
        username = user_data.username,
        hashed_password = hash_password(user_data.password),
        phone = user_data.phone,
        email = user_data.email,
    )
    session.add(user_context)
    session.commit()
    session.refresh(user_context)
    return user_context


@router.get("/list", response_model=list[ReadUser])  # user/list
async def get_users(current_user: Annotated[User, Depends(get_current_user)], session: SessionDep):
    """
    Get a list of users. Requires authentication.
    """
    if current_user is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Not authenticated")
    user_list = session.exec(select(User)).all()
    return user_list

@router.post("/login")
def login_user(user: LoginUser, session: SessionDep):
    username = user.username 
    password = user.password
    
    user = session.exec(select(User).where(User.username == username)).first()
    if not user or not verify_password(password, user.hashed_password):
        return {"error": "Invalid username or password."}
    
    to_encode = {
        "sub": user.username,
        "id": user.id,
    }

    encoded_jwt = generate_access_token(to_encode, expires_delta=30)
    return {"access_token": encoded_jwt, "token_type": "bearer"}
