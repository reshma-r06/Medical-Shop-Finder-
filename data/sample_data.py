import pandas as pd
import random
from sqlalchemy.orm import Session
from backend.app.models.database import MedicalShop, MedicineInventory, engine, SessionLocal

def create_sample_data():
    """Create sample medical shops and inventory data"""
    
    # Sample medical shops in Delhi area
    medical_shops_data = [
        {
            "name": "Apollo Pharmacy",
            "latitude": 28.6129,
            "longitude": 77.2295,
            "address": "Connaught Place, New Delhi",
            "phone": "+91-11-12345678",
            "operating_hours": {"open": "08:00", "close": "22:00"},
            "rating": 4.5
        },
        {
            "name": "MedPlus Mart",
            "latitude": 28.6329,
            "longitude": 77.2195,
            "address": "Karol Bagh, Delhi",
            "phone": "+91-11-23456789",
            "operating_hours": {"open": "09:00", "close": "21:00"},
            "rating": 4.2
        },
        {
            "name": "Fortis Pharmacy",
            "latitude": 28.6029,
            "longitude": 77.2395,
            "address": "Saket, New Delhi",
            "phone": "+91-11-34567890",
            "operating_hours": {"open": "08:30", "close": "22:30"},
            "rating": 4.7
        },
        {
            "name": "City Medicos",
            "latitude": 28.6229,
            "longitude": 77.2495,
            "address": "Lajpat Nagar, Delhi",
            "phone": "+91-11-45678901",
            "operating_hours": {"open": "07:00", "close": "23:00"},
            "rating": 4.0
        },
        {
            "name": "Health Plus",
            "latitude": 28.6429,
            "longitude": 77.2095,
            "address": "Rajouri Garden, Delhi",
            "phone": "+91-11-56789012",
            "operating_hours": {"open": "08:00", "close": "20:00"},
            "rating": 4.3
        }
    ]
    
    # Common medicines
    medicines = [
        {"name": "Paracetamol", "generic_name": "Acetaminophen", "brand": "Crocin"},
        {"name": "Ibuprofen", "generic_name": "Ibuprofen", "brand": "Brufen"},
        {"name": "Amoxicillin", "generic_name": "Amoxicillin", "brand": "Mox"},
        {"name": "Azithromycin", "generic_name": "Azithromycin", "brand": "Azee"},
        {"name": "Cetirizine", "generic_name": "Cetirizine", "brand": "Zyrtec"},
        {"name": "Vitamin C", "generic_name": "Ascorbic Acid", "brand": "Celin"},
        {"name": "Metformin", "generic_name": "Metformin", "brand": "Glycomet"},
        {"name": "Aspirin", "generic_name": "Acetylsalicylic Acid", "brand": "Ecosprin"},
        {"name": "Omeprazole", "generic_name": "Omeprazole", "brand": "Omez"},
        {"name": "Atorvastatin", "generic_name": "Atorvastatin", "brand": "Atorva"}
    ]
    
    db = SessionLocal()
    
    try:
        # Clear existing data
        db.query(MedicineInventory).delete()
        db.query(MedicalShop).delete()
        db.commit()
        
        # Add medical shops
        for shop_data in medical_shops_data:
            shop = MedicalShop(**shop_data)
            db.add(shop)
        
        db.commit()
        
        # Get all shops
        shops = db.query(MedicalShop).all()
        
        # Add medicine inventory
        for shop in shops:
            # Each shop gets 5-8 random medicines
            shop_medicines = random.sample(medicines, random.randint(5, 8))
            
            for med in shop_medicines:
                inventory = MedicineInventory(
                    shop_id=shop.id,
                    medicine_name=med["name"],
                    brand=med["brand"],
                    generic_name=med["generic_name"],
                    price=round(random.uniform(10, 500), 2),
                    stock_quantity=random.randint(0, 100)
                )
                db.add(inventory)
        
        db.commit()
        print("Sample data created successfully!")
        
    except Exception as e:
        print(f"Error creating sample data: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    create_sample_data()