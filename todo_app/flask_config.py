import os

class Config:
    """Base configuration variables."""
    MONGO_PASSWORD = os.environ.get('MONGO_PASSWORD')
    if not MONGO_PASSWORD:
        raise ValueError("No MONGO_PASSWORD set for Flask application. Did you follow the setup instructions?")
