from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(min_length=6)

class UserOut(BaseModel):
    id: int
    email: EmailStr
    class Config:
        from_attributes = True

class ProfileIn(BaseModel):
    display_name: Optional[str] = None
    bio: Optional[str] = None
    lat: Optional[float] = None
    lon: Optional[float] = None
    is_mentor: bool = False
    skills: List[str] = []

class ProfileOut(ProfileIn):
    user_id: int
    class Config:
        from_attributes = True

class RatingIn(BaseModel):
    ratee_id: int
    stars: int = Field(ge=1, le=5)
    comment: Optional[str] = None

class MessageIn(BaseModel):
    receiver_id: int
    content: str
