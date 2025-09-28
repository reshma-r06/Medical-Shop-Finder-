import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from typing import List, Dict
import joblib
import os

class RecommendationService:
    def __init__(self):
        self.vectorizer = TfidfVectorizer(stop_words='english')
        self.medicine_similarity = None
        self.medicines_df = None
        
    def train_recommendation_model(self, medicines_data: List[Dict]):
        """Train medicine recommendation model"""
        self.medicines_df = pd.DataFrame(medicines_data)
        
        # Combine features for similarity calculation
        features = self.medicines_df['medicine_name'] + " " + \
                  self.medicines_df['generic_name'].fillna('') + " " + \
                  self.medicines_df['brand'].fillna('')
        
        # Create TF-IDF matrix
        tfidf_matrix = self.vectorizer.fit_transform(features)
        
        # Calculate cosine similarity
        self.medicine_similarity = cosine_similarity(tfidf_matrix, tfidf_matrix)
        
        # Save model
        os.makedirs('../../models/trained_models', exist_ok=True)
        joblib.dump({
            'vectorizer': self.vectorizer,
            'similarity_matrix': self.medicine_similarity,
            'medicines_df': self.medicines_df
        }, '../../models/trained_models/recommendation_model.pkl')
    
    def load_model(self):
        """Load trained recommendation model"""
        try:
            model_data = joblib.load('../../models/trained_models/recommendation_model.pkl')
            self.vectorizer = model_data['vectorizer']
            self.medicine_similarity = model_data['similarity_matrix']
            self.medicines_df = model_data['medicines_df']
            return True
        except:
            return False
    
    def get_similar_medicines(self, medicine_name: str, top_k: int = 5) -> List[Dict]:
        """Get similar medicine recommendations"""
        if self.medicine_similarity is None:
            if not self.load_model():
                return []
        
        # Find medicine index
        medicine_idx = self.medicines_df[
            self.medicines_df['medicine_name'].str.contains(medicine_name, case=False)
        ].index
        
        if len(medicine_idx) == 0:
            return []
        
        # Get similarity scores
        similarity_scores = list(enumerate(self.medicine_similarity[medicine_idx[0]]))
        
        # Sort by similarity
        similarity_scores = sorted(similarity_scores, key=lambda x: x[1], reverse=True)
        
        # Get top k similar medicines (excluding itself)
        similar_indices = [i[0] for i in similarity_scores[1:top_k+1]]
        
        recommendations = []
        for idx in similar_indices:
            medicine = self.medicines_df.iloc[idx]
            recommendations.append({
                'medicine_name': medicine['medicine_name'],
                'brand': medicine['brand'],
                'generic_name': medicine['generic_name'],
                'similarity_score': similarity_scores[idx][1]
            })
        
        return recommendations