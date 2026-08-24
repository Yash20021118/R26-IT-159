from flask import Flask
from flask_pymongo import PyMongo
from dotenv import load_dotenv
import os

load_dotenv()
mongo = PyMongo()



def create_app():
    app = Flask(__name__, template_folder='views', static_folder='../static')
    app.config['SECRET_KEY'] = os.getenv('SECRET_KEY', 'smartseed_super_secret_key_2026')
    app.config['MONGO_URI'] = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smartseed_db')
    
    try:
        mongo.init_app(app)
        # Test server availability
        mongo.cx.server_info()
    except Exception as e:
        print("[INFO] MongoDB server connection failed. Initializing in-memory mock database for seamless execution...")
        import mongomock
        import bcrypt
        from datetime import datetime
        
        mock_client = mongomock.MongoClient()
        mongo.db = mock_client.smartseed_db

        # Auto-seed demo accounts into mock database
        farmer_pw = bcrypt.hashpw(b"farmer123", bcrypt.gensalt())
        admin_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
        
        mongo.db.admins.insert_one({
            "name": "Super Admin", "email": "admin@smartseed.com", "password_hash": admin_pw
        })
        user_res = mongo.db.users.insert_one({
            "name": "Sunil Perera", "email": "farmer@smartseed.com", "password_hash": farmer_pw, "created_at": datetime.utcnow()
        })
        farm_res = mongo.db.farms.insert_one({
            "user_id": user_res.inserted_id,
            "farm_name": "Green Valley Estate",
            "location": {"lat": 6.9271, "lng": 79.8612, "district": "Colombo", "zone": "Wet Zone"},
            "agro_zone": "WL1", "altitude": 25.0,
            "sensors": {"device_id": "DEV_001"},
            "crop_type": "Rice"
        })
        mongo.db.sensor_readings.insert_one({
            "device_id": "DEV_001", "farm_id": farm_res.inserted_id, "timestamp": datetime.utcnow(),
            "soil_moisture": 55.0, "ph_level": 6.5, "temperature": 24.5,
            "nitrogen": 90.0, "phosphorus": 42.0, "potassium": 43.0,
            "predicted_soil": "Noncalcic Brown soils", "confidence": 94.2
        })
        print("[INFO] Mock DB Auto-Seeded: farmer@smartseed.com / farmer123")

    with app.app_context():
        from app.controllers.admin_controller import admin_bp
        from app.controllers.farmer_controller import farmer_bp
        from app.controllers.api_controller import api_bp
        
        app.register_blueprint(admin_bp)
        app.register_blueprint(farmer_bp)
        app.register_blueprint(api_bp)
        
        return app