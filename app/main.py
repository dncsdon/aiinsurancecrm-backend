from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import stripe
import os
from dotenv import load_dotenv
from . import crud, models, schemas
from .database import SessionLocal, engine
from .ai import qualify_lead

load_dotenv()
models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="AI Insurance CRM API")

# CORS for your Vercel frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["https://aiinsurancecrm.vercel.app", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

stripe.api_key = os.getenv("STRIPE_SECRET_KEY")

# Dependency
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/register", response_model=schemas.LoginResponse)
async def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = crud.create_user(db=db, user=user)
    return {"user_id": db_user.id, "sms_credits": db_user.sms_credits}

@app.post("/leads", response_model=schemas.LeadResponse)
async def create_lead(lead: schemas.LeadCreate, user_id: int, db: Session = Depends(get_db)):
    # AI Magic ✨
    ai_result = await qualify_lead(lead.dict())
    
    # Save scored lead
    db_lead = crud.create_lead(db, lead, user_id, ai_result["score"])
    return db_lead

@app.get("/leads/{user_id}")
async def get_leads(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    leads = crud.get_leads(db, user_id, skip=skip, limit=limit)
    return leads

@app.post("/stripe/webhook")
async def stripe_webhook(request: Request):
    payload = await request.body()
    sig_header = request.headers.get("stripe-signature")
    # Handle Stripe webhooks for subscriptions
    return {"status": "success"}
