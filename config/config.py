# config/config.py
import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///personality_predictor.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SECRET_KEY = os.urandom(24)
