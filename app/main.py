from fastapi import FastAPI, WebSocket, Depends
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
import os
from dotenv import load_dotenv
from pydantic import BaseModel
from typing import List

# Load environment variables
load_dotenv()
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./orders.db")

# Database setup
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Define Order Model
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(String)

# ✅ Force database reset before app starts
def reset_database():
    with engine.begin() as conn:
        Base.metadata.drop_all(bind=conn)  # Clears old tables
        Base.metadata.create_all(bind=conn)  # Recreates tables

# ✅ Reset DB on startup to ensure fresh state
reset_database()

# FastAPI app
app = FastAPI()

# Dependency for database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# Pydantic Model for Order Request
class OrderCreate(BaseModel):
    symbol: str
    price: float
    quantity: int
    order_type: str

# Create Order (Fix: Accept JSON instead of query params)
@app.post("/orders", response_model=OrderCreate)
def create_order(order: OrderCreate, db: Session = Depends(get_db)):
    new_order = Order(**order.model_dump())  # ✅ Fix for Pydantic v2
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# Get All Orders (Ensure Clean Response)
@app.get("/orders", response_model=List[OrderCreate])
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return orders  # ✅ API returns structured response
