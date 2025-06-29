from sqlmodel import Field, SQLModel

class User(SQLModel, table=True):
    id: int = Field(primary_key=True, index=True)
    first_name: str
    last_name: str
    phone: str
    email: str = Field(default=None, nullable=True)
    address: str 
    gender: str

class UserCreateModel(SQLModel):
    first_name: str
    last_name: str
    phone: str
    email: str = Field(default=None, nullable=True)
    address: str 
    gender: str
    