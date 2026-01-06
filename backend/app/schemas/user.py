
from typing import Optional
from pydantic import BaseModel, EmailStr

# Shared properties
class UserBase(BaseModel):
    email: EmailStr

# Properties to receive via API on creation
class UserCreate(UserBase):
    password: str
    full_name: Optional[str] = None

# Properties to return to client
class UserResponse(UserBase):
    id: int
    full_name: Optional[str] = None
    is_active: bool

    class Config:
        from_attributes = True
