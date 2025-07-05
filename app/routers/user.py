from models.user import User
from schemas.user import CreateUser, ReadUser
from database import get_session    
from typing import Annotated
from sqlmodel import Session, select
from fastapi import APIRouter, Depends
from core.security import hash_password, verify_password

router = APIRouter(prefix="/user", tags=["User"])
SessionDep = Annotated[Session, Depends(get_session)]

@router.post("/register", response_model=ReadUser)   # user/register
def create_user(user: CreateUser, session: SessionDep):
    user_context  = User(
        first_name = user.first_name,
        last_name = user.last_name,
        hashed_password = hash_password(user.password),
        phone = user.phone,
        email = user.email,
    )
    session.add(user_context)
    session.commit()
    session.refresh(user_context)
    return user_context


@router.get("/list", response_model=list[ReadUser])  # user/list
def get_users(session: SessionDep):    
    user_list = session.exec(select(User)).all()
    return user_list