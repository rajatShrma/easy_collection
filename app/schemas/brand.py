from pydantic import BaseModel
from sqlmodel import SQLModel, Field

class BrandCreate(BaseModel):
    name: str
    origin_country: str
    description: str
    established_year: int
    is_active: bool = True

class BrandRead(BaseModel):
    id: int
    name: str
    origin_country: str
    description: str
    established_year: int
    is_active: bool


class UpdateBrandModel(SQLModel):
    name: str = Field(nullable=True, default=None)
    origin_country: str = Field(nullable=True, default=None)
    description: str = Field(nullable= True, default=None)
    message: str= Field(nullable=True, default=None)
    