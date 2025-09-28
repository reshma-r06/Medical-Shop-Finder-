import math
from typing import List, Tuple
from sqlalchemy.orm import Session
from ..models.database import MedicalShop

class LocationService:
    @staticmethod
    def calculate_distance(lat1: float, lon1: float, lat2: float, lon2: float) -> float:
        """Calculate distance between two coordinates using Haversine formula"""
        R = 6371  # Earth radius in kilometers
        
        dlat = math.radians(lat2 - lat1)
        dlon = math.radians(lon2 - lon1)
        
        a = (math.sin(dlat/2) * math.sin(dlat/2) +
             math.cos(math.radians(lat1)) * math.cos(math.radians(lat2)) *
             math.sin(dlon/2) * math.sin(dlon/2))
        
        c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
        distance = R * c
        
        return distance

    @staticmethod
    def find_nearby_shops(db: Session, user_lat: float, user_lon: float, 
                         radius_km: float = 5.0) -> List[Tuple[MedicalShop, float]]:
        """Find shops within specified radius"""
        shops_with_distance = []
        
        all_shops = db.query(MedicalShop).all()
        
        for shop in all_shops:
            distance = LocationService.calculate_distance(
                user_lat, user_lon, shop.latitude, shop.longitude
            )
            
            if distance <= radius_km:
                shops_with_distance.append((shop, distance))
        
        # Sort by distance
        shops_with_distance.sort(key=lambda x: x[1])
        
        return shops_with_distance