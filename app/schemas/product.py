from pydantic import BaseModel
from typing import Optional
from sqlmodel import Field, SQLModel

class ProductCreateModel(BaseModel):
    name: str
    company: str
    description: Optional[str] = None
    price: float
    expiry_date: int

class ProductReadModel(BaseModel):
    id:int = Field(primary_key=True, index=True)
    name: str
    company: str
    description: Optional[str]= None
    price: float
    expiry_date: int

class UpdateProductModel(SQLModel):
    name: str = Field(nullable=True, default=None)
    company: str = Field(nullable=True, default=None)
    description: str = Field(nullable= True, default=None)
    price: float= Field(nullable=True, default=None)
    expiry_date: int = Field(nullable=True, default=None)