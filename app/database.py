from sqlmodel import SQLModel, Session, create_engine


sqlite_url = "sqlite:///./shop_online.db"
engine = create_engine(sqlite_url, connect_args={"check_same_thread": False})

def create_db_and_tables():
    SQLModel.metadata.create_all(engine)

def get_session():
    with Session(engine) as session:
        yield session
