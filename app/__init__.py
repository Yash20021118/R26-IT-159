from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()
mongo = PyMongo()



def create_app():
    app = Flask(__name__, template_folder='views', static_folder='../static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI')
    
    mongo.init_app(app)
    
    with app.app_context():
        from app.controllers.admin_controller import admin_bp
        from app.controllers.farmer_controller import farmer_bp
        from app.controllers.api_controller import api_bp
        from app.controllers.chat_controller import chat_bp
        
        app.register_blueprint(admin_bp)
        app.register_blueprint(farmer_bp)
        app.register_blueprint(api_bp)
        app.register_blueprint(chat_bp)
        
        return app