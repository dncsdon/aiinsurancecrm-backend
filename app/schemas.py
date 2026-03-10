from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class LeadCreate(BaseModel):
    name: str
    email: Optional[str]
    phone: str
    notes: Optional[str] = ""

class LeadResponse(BaseModel):
    id: int
    name: str
    email: Optional[str]
    phone: str
    ai_score: float
    status: str
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCreate(BaseModel):
    email: str

class LoginResponse(BaseModel):
    user_id: int
    sms_credits: int
