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

# FastAPI app
app = FastAPI()

# Define Order Model
class Order(Base):
    __tablename__ = "orders"
    id = Column(Integer, primary_key=True, index=True)
    symbol = Column(String, index=True)
    price = Column(Float)
    quantity = Column(Integer)
    order_type = Column(String)


@app.on_event("startup")
def startup():
    Base.metadata.create_all(bind=engine)

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
    new_order = Order(**order.model_dump())  
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    return new_order

# Get All Orders
@app.get("/orders")
def get_orders(db: Session = Depends(get_db)):
    orders = db.query(Order).all()
    return [  
        {
            "symbol": order.symbol,
            "price": order.price,
            "quantity": order.quantity,
            "order_type": order.order_type,
        }
        for order in orders
    ]

