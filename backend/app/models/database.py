from sqlalchemy import create_engine, Column, Integer, String, Float, Text, JSON, DateTime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import datetime

Base = declarative_base()

class MedicalShop(Base):
    __tablename__ = "medical_shops"
    
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), nullable=False)
    latitude = Column(Float, nullable=False)
    longitude = Column(Float, nullable=False)
    address = Column(Text)
    phone = Column(String(20))
    operating_hours = Column(JSON)
    rating = Column(Float)
    last_updated = Column(DateTime, default=datetime.datetime.utcnow)

class MedicineInventory(Base):
    __tablename__ = "medicine_inventory"
    
    id = Column(Integer, primary_key=True, index=True)
    shop_id = Column(Integer, nullable=False)
    medicine_name = Column(String(255), nullable=False)
    brand = Column(String(255))
    price = Column(Float)
    stock_quantity = Column(Integer)
    generic_name = Column(String(255))

# SQLite database

# Use absolute path for database file
import os
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../medical_shops.db'))
print(f"[DEBUG] Using SQLite database file at: {db_path}")
SQLALCHEMY_DATABASE_URL = f"sqlite:///{db_path}"
engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_tables():
    Base.metadata.create_all(bind=engine)