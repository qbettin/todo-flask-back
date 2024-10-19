import os

SQLALCHEMY_DATABASE_URI = os.getenv('DATABASE_URI')  # SQLite database
SQLALCHEMY_TRACK_MODIFICATIONS = False
JWT_SECRET_KEY = os.getenv('JWT_SECRET')  # Replace with your own secret
