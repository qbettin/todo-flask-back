import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
class Config:
    # Use the environment variable for the database URI, defaulting to a local SQLite file
    SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')  # SQLite database
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET')  # Replace with your own secret
