from sqlalchemy import Column, Integer, String, Float, DateTime, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from .database import Base

class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    stripe_customer_id = Column(String)
    sms_credits = Column(Integer, default=500)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

class Lead(Base):
    __tablename__ = "leads"
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    name = Column(String)
    email = Column(String)
    phone = Column(String)
    ai_score = Column(Float)  # 0-100 hotness score
    status = Column(String, default="new")  # new, qualified, booked, closed
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    user = relationship("User", back_populates="leads")

User.leads = relationship("Lead", back_populates="user")
