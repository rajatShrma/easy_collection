from pydantic import BaseModel

class CreateUser(BaseModel):
    first_name: str
    last_name: str
    username: str
    phone: str
    email: str = None
    password: str

class ReadUser(BaseModel):
    id: int
    first_name: str
    last_name: str
    username: str
    phone: str
    email: str = None

class LoginUser(BaseModel):
    username: str
    password: str