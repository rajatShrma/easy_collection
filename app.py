from fastapi import FastAPI, Depends
from typing import Annotated
from fastapi_sqlmodel import DBSessionMiddleware, db
from sqlmodel import create_engine, SQLModel, Session, select

from user.models import User, UserCreateModel

app = FastAPI()

sqlite_url = "sqlite:///./muna_collection_db.db"
app.add_middleware(DBSessionMiddleware, db_url=sqlite_url)

connect_args = {"check_same_thread": False}
engine = create_engine(sqlite_url, connect_args=connect_args)


def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_session)]

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.post("/user/")
def create_user(user: UserCreateModel, session: SessionDep):
    user_context  = User(
        first_name = user.first_name,
        last_name = user.last_name,
        phone = user.phone,
        email = user.email,
        address = user.address,
        gender = user.gender
    )
    session.add(user_context)
    session.commit()
    session.refresh(user_context)
    return user_context


@app.get("/users")
def get_users(session: SessionDep):    
    user_list = session.exec(select(User)).all()
    return user_list