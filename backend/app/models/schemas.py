from pydantic import BaseModel
from typing import List, Optional, Dict, Any
from datetime import datetime

class MedicalShopBase(BaseModel):
    name: str
    latitude: float
    longitude: float
    address: Optional[str] = None
    phone: Optional[str] = None
    operating_hours: Optional[Dict[str, Any]] = None
    rating: Optional[float] = None

class MedicalShopCreate(MedicalShopBase):
    pass

class MedicalShopResponse(MedicalShopBase):
    id: int
    distance: Optional[float] = None
    last_updated: datetime
    
    class Config:
        from_attributes = True

class MedicineInventoryBase(BaseModel):
    shop_id: int
    medicine_name: str
    brand: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: int
    generic_name: Optional[str] = None

class SearchRequest(BaseModel):
    latitude: float
    longitude: float
    medicine_name: Optional[str] = None
    radius_km: float = 5.0
    max_results: int = 10

class RecommendationRequest(BaseModel):
    medicine_name: str
    top_k: int = 5