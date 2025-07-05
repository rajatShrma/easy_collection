from datetime import datetime
from sqlmodel import SQLModel, Field

class ContactMessageModel(SQLModel):
    full_name: str = Field(index=True, max_length=100)
    email: str = Field(index=True, max_length=100)
    subject: str = Field(max_length=150)
    message: str
    



class ContactMessage(ContactMessageModel, table = True):
    id: int = Field(primary_key = True, index = True)
    created_at: datetime = Field(default_factory=datetime.utcnow)


class UpdateContactMessageModel(SQLModel):
    full_name: str = Field(nullable=True, default=None)
    email: str = Field(nullable=True, default=None)
    subject: str = Field(nullable= True, default=None)
    message: str= Field(nullable=True, default=None)
    