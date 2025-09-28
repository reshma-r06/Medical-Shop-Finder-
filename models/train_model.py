import pandas as pd
import joblib
from backend.app.services.recommendation_service import RecommendationService
from sqlalchemy import create_engine
import sys
import os

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

def train_recommendation_model():
    """Train the medicine recommendation model"""
    
    # Connect to database using shared engine
    from backend.app.models.database import engine
    
    # Load medicine data
    query = "SELECT DISTINCT medicine_name, generic_name, brand FROM medicine_inventory"
    medicines_df = pd.read_sql(query, engine)
    
    # Prepare data for training
    medicines_data = medicines_df.to_dict('records')
    
    # Train model
    recommender = RecommendationService()
    recommender.train_recommendation_model(medicines_data)
    
    print("Recommendation model trained and saved successfully!")

if __name__ == "__main__":
    train_recommendation_model()