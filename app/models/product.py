from sqlmodel import Field, SQLModel
from typing import Optional

class Product(SQLModel, table=True):
    id:int = Field(primary_key=True, index=True)
    name: str
    company: str
    description: Optional[str]= None
    price: float
    expiry_date: int
    