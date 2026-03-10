from sqlalchemy.orm import Session
from . import models, schemas

def create_user(db: Session, user: schemas.UserCreate):
    db_user = models.User(email=user.email)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user

def create_lead(db: Session, lead: schemas.LeadCreate, user_id: int, ai_score: float):
    db_lead = models.Lead(
        **lead.dict(),
        user_id=user_id,
        ai_score=ai_score
    )
    db.add(db_lead)
    db.commit()
    db.refresh(db_lead)
    return db_lead

def get_leads(db: Session, user_id: int, skip: int = 0, limit: int = 100):
    return db.query(models.Lead).filter(models.Lead.user_id == user_id).offset(skip).limit(limit).all()
