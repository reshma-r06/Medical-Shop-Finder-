import streamlit as st
import requests
import pandas as pd
import folium
from streamlit_folium import folium_static
from geopy.geocoders import Nominatim
import time

# Configure page
st.set_page_config(
    page_title="Medical Shop Finder",
    page_icon="🏥",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .shop-card {
        padding: 1rem;
        border-radius: 10px;
        border: 1px solid #ddd;
        margin: 0.5rem 0;
        background-color: #f9f9f9;
    }
    .medicine-item {
        background-color: #e8f4fd;
        padding: 0.5rem;
        margin: 0.2rem 0;
        border-radius: 5px;
    }
</style>
""", unsafe_allow_html=True)

# Backend API URL
API_BASE_URL = "http://localhost:8000"

class MedicalShopFinder:
    def __init__(self):
        self.geolocator = Nominatim(user_agent="medical_shop_finder")
    
    def get_current_location(self):
        """Get current location using IP or manual input"""
        try:
            # For demo, we'll use a default location
            return (28.6139, 77.2090)  # Default to Delhi
        except:
            return (28.6139, 77.2090)
    
    def geocode_address(self, address):
        """Convert address to coordinates"""
        try:
            location = self.geolocator.geocode(address)
            if location:
                return (location.latitude, location.longitude)
        except:
            pass
        return None

def main():
    st.markdown('<div class="main-header">🏥 Medical Shop Finder</div>', unsafe_allow_html=True)
    
    # Initialize finder
    finder = MedicalShopFinder()
    
    # Sidebar for search parameters
    with st.sidebar:
        st.header("🔍 Search Parameters")
        
        # Location input
        location_method = st.radio("Location Method:", ["Use Current Location", "Enter Address"])
        
        if location_method == "Use Current Location":
            user_lat, user_lon = finder.get_current_location()
            st.success(f"Using location: {user_lat:.4f}, {user_lon:.4f}")
        else:
            address = st.text_input("Enter your address:")
            if address:
                coords = finder.geocode_address(address)
                if coords:
                    user_lat, user_lon = coords
                    st.success(f"Location found: {user_lat:.4f}, {user_lon:.4f}")
                else:
                    st.error("Could not find location. Using default.")
                    user_lat, user_lon = finder.get_current_location()
            else:
                user_lat, user_lon = finder.get_current_location()
        
        # Medicine search
        medicine_name = st.text_input("Medicine Name (optional):")
        
        # Search radius
        radius_km = st.slider("Search Radius (km):", 1.0, 20.0, 5.0)
        
        # Max results
        max_results = st.slider("Max Results:", 5, 50, 10)
        
        if st.button("🔍 Search Medical Shops", type="primary"):
            with st.spinner("Searching for medical shops..."):
                search_params = {
                    "latitude": user_lat,
                    "longitude": user_lon,
                    "medicine_name": medicine_name if medicine_name else None,
                    "radius_km": radius_km,
                    "max_results": max_results
                }
                
                try:
                    response = requests.post(f"{API_BASE_URL}/api/v1/search", json=search_params)
                    if response.status_code == 200:
                        st.session_state.search_results = response.json()
                    else:
                        st.error("Error searching for medical shops")
                except requests.exceptions.RequestException:
                    st.error("Could not connect to backend server")
    
    # Main content area
    col1, col2 = st.columns([1, 1])
    
    with col1:
        st.subheader("📍 Search Results")
        
        if 'search_results' in st.session_state and st.session_state.search_results:
            results = st.session_state.search_results
            
            for shop in results:
                with st.container():
                    st.markdown(f"""
                    <div class="shop-card">
                        <h3>🏪 {shop['name']}</h3>
                        <p><strong>📍 Distance:</strong> {shop['distance']} km</p>
                        <p><strong>📞 Phone:</strong> {shop.get('phone', 'N/A')}</p>
                        <p><strong>⭐ Rating:</strong> {shop.get('rating', 'N/A')}</p>
                        <p><strong>🏠 Address:</strong> {shop.get('address', 'N/A')}</p>
                    """, unsafe_allow_html=True)
                    
                    if shop['available_medicines']:
                        st.markdown("<strong>💊 Available Medicines:</strong>", unsafe_allow_html=True)
                        for med in shop['available_medicines']:
                            st.markdown(f"""
                            <div class="medicine-item">
                                {med['name']} - {med.get('brand', 'Generic')} 
                                💰 ${med.get('price', 'N/A')} | 📦 {med.get('stock', 0)} in stock
                            </div>
                            """, unsafe_allow_html=True)
                    
                    st.markdown("</div>", unsafe_allow_html=True)
                    st.markdown("---")
        else:
            st.info("Enter search parameters and click 'Search Medical Shops' to find nearby pharmacies.")
    
    with col2:
        st.subheader("🗺️ Map View")
        
        if 'search_results' in st.session_state and st.session_state.search_results:
            # Create map centered on user location
            m = folium.Map(location=[user_lat, user_lon], zoom_start=12)
            
            # Add user location marker
            folium.Marker(
                [user_lat, user_lon],
                popup="Your Location",
                icon=folium.Icon(color='red', icon='user')
            ).add_to(m)
            
            # Add shop markers
            for shop in st.session_state.search_results:
                folium.Marker(
                    [shop['latitude'], shop['longitude']],
                    popup=f"{shop['name']}\nDistance: {shop['distance']}km",
                    icon=folium.Icon(color='blue', icon='plus')
                ).add_to(m)
            
            # Display map
            folium_static(m, width=600, height=500)
        else:
            # Show default map
            m = folium.Map(location=[user_lat, user_lon], zoom_start=12)
            folium.Marker(
                [user_lat, user_lon],
                popup="Your Location",
                icon=folium.Icon(color='red', icon='user')
            ).add_to(m)
            folium_static(m, width=600, height=500)
    
    # Recommendations section
    if medicine_name:
        st.subheader("💡 Medicine Recommendations")
        if st.button("Get Similar Medicines"):
            with st.spinner("Finding similar medicines..."):
                try:
                    response = requests.post(
                        f"{API_BASE_URL}/api/v1/recommendations",
                        json={"medicine_name": medicine_name, "top_k": 5}
                    )
                    if response.status_code == 200:
                        recommendations = response.json()['recommendations']
                        if recommendations:
                            rec_df = pd.DataFrame(recommendations)
                            st.dataframe(rec_df)
                        else:
                            st.info("No recommendations found for this medicine.")
                    else:
                        st.error("Error getting recommendations")
                except requests.exceptions.RequestException:
                    st.error("Could not connect to backend server")

if __name__ == "__main__":
    main()