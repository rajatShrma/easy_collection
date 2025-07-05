from sqlmodel import Field, SQLModel
from typing import Optional


class BrandBaseModel(SQLModel):
    name : str
    origin_country : str 
    description : Optional[str] = None 
    established_year : str
    is_active : bool = True


class Brand(BrandBaseModel, table = True):
    id: int = Field(primary_key = True, index = True)
    
 