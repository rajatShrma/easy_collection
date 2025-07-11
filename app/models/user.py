from sqlmodel import SQLModel, Field

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    first_name: str
    last_name: str
    hashed_password: str
    phone: str
    email: str = Field(default=None, nullable=True)