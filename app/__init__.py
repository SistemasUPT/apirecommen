# app/__init__.py
from flask import Flask
from flask_cors import CORS
from .config import Config

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    
    CORS(app)  # Habilita CORS para todas las rutas
    
    # Registrar rutas
    from .routes.recommend import bp as recommend_bp
    app.register_blueprint(recommend_bp)
    
    return app
