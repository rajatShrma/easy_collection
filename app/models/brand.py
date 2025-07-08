from sqlmodel import Field, SQLModel
from typing import Optional
    

class Brand(SQLModel, table = True):
    id: int = Field(primary_key = True, index = True)
    name : str
    origin_country : str 
    description : Optional[str] = None 
    established_year : str
    is_active : bool = True
