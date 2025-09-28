import subprocess
import sys
import os
import time
import webbrowser
import threading

def run_backend():
    """Run the FastAPI backend server"""
    backend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'backend')
    os.chdir(backend_dir)
    subprocess.run([sys.executable, "-m", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"])

def run_frontend():
    """Run the Streamlit frontend"""
    frontend_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'frontend')
    os.chdir(frontend_dir)
    subprocess.run([sys.executable, "-m", "streamlit", "run", "app.py"])

if __name__ == "__main__":
    print("🚀 Starting Medical Shop Finder Application...")
    # Ensure database tables are created
    from backend.app.models.database import create_tables
    create_tables()

    # Create sample data first
    print("📊 Creating sample data...")
    from data.sample_data import create_sample_data
    create_sample_data()

    # Train recommendation model
    print("🤖 Training recommendation model...")
    from models.train_model import train_recommendation_model
    train_recommendation_model()

    print("✅ Setup completed!")
    print("\n🌐 Starting servers...")
    print("Backend API: http://localhost:8000")
    print("Frontend App: http://localhost:8501")
    print("\nPress Ctrl+C to stop all servers")

    # Start backend in a separate thread
    backend_thread = threading.Thread(target=run_backend)
    backend_thread.daemon = True
    backend_thread.start()

    # Wait for backend to start
    time.sleep(5)

    # Start frontend
    run_frontend()