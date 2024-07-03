# backend/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_cors import CORS
from config.config import Config

db = SQLAlchemy()

def create_app():
    app = Flask(__name__, 
                static_folder="../frontend/static", 
                template_folder="templates")
    app.config.from_object(Config)
    CORS(app)
    db.init_app(app)

    with app.app_context():
        from . import routes
        db.create_all()

    return app
