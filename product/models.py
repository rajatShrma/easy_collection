from sqlmodel import Field, SQLModel
from typing import Optional

class Product(SQLModel, table=True):
    number:int = Field(primary_key=True, index=True)
    name: str
    company: str
    description: Optional[str]= None
    price: float
    expiry_date: int
    
class ProductCreateModel(SQLModel):
    name: str
    company: str
    description: Optional[str] = None
    price: float
    expiry_date: int