from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
from typing import List

from .models.database import get_db, create_tables
from .models.schemas import (
    MedicalShopCreate, MedicalShopResponse, SearchRequest, 
    RecommendationRequest, MedicineInventoryBase
)
from .services.search_service import SearchService
from .services.recommendation_service import RecommendationService

app = FastAPI(title="Medical Shop Finder API", version="1.0.0")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize services
recommendation_service = RecommendationService()

@app.on_event("startup")
async def startup_event():
    create_tables()
    recommendation_service.load_model()

@app.get("/")
async def root():
    return {"message": "Medical Shop Finder API", "version": "1.0.0"}

@app.post("/api/v1/search", response_model=List[dict])
async def search_medical_shops(request: SearchRequest, db: Session = Depends(get_db)):
    """Search for nearby medical shops"""
    try:
        results = SearchService.search_medical_shops(
            db=db,
            user_lat=request.latitude,
            user_lon=request.longitude,
            medicine_name=request.medicine_name,
            radius_km=request.radius_km,
            max_results=request.max_results
        )
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/shops", response_model=List[MedicalShopResponse])
async def get_all_shops(db: Session = Depends(get_db)):
    """Get all medical shops"""
    shops = db.query(MedicalShop).all()
    return shops

@app.post("/api/v1/recommendations")
async def get_medicine_recommendations(request: RecommendationRequest):
    """Get medicine recommendations"""
    try:
        recommendations = recommendation_service.get_similar_medicines(
            request.medicine_name, request.top_k
        )
        return {"recommendations": recommendations}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/api/v1/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)