from sqlalchemy.orm import Session
from typing import List, Optional
from ..models.database import MedicalShop, MedicineInventory
from .location_service import LocationService

class SearchService:
    @staticmethod
    def search_medical_shops(db: Session, user_lat: float, user_lon: float,
                           medicine_name: Optional[str] = None,
                           radius_km: float = 5.0,
                           max_results: int = 10) -> List[dict]:
        """Search for medical shops with optional medicine filter"""
        
        # Find nearby shops
        nearby_shops = LocationService.find_nearby_shops(db, user_lat, user_lon, radius_km)
        
        results = []
        
        for shop, distance in nearby_shops[:max_results]:
            shop_data = {
                "id": shop.id,
                "name": shop.name,
                "latitude": shop.latitude,
                "longitude": shop.longitude,
                "address": shop.address,
                "phone": shop.phone,
                "operating_hours": shop.operating_hours,
                "rating": shop.rating,
                "distance": round(distance, 2),
                "available_medicines": []
            }
            
            # If medicine name is specified, check availability
            if medicine_name:
                medicines = db.query(MedicineInventory).filter(
                    MedicineInventory.shop_id == shop.id,
                    MedicineInventory.medicine_name.ilike(f"%{medicine_name}%")
                ).all()
                
                if medicines:
                    shop_data["available_medicines"] = [
                        {
                            "name": med.medicine_name,
                            "brand": med.brand,
                            "price": med.price,
                            "stock": med.stock_quantity
                        }
                        for med in medicines
                    ]
                    results.append(shop_data)
            else:
                results.append(shop_data)
        
        return results