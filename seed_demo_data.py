import bcrypt
from pymongo import MongoClient
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
mongo_uri = os.getenv('MONGO_URI', 'mongodb://localhost:27017/smartseed_db')

if mongo_uri.startswith('mongomock://'):
    import mongomock
    client = mongomock.MongoClient()
    db = client.smartseed_db
    print("[INFO] Using In-Memory mongomock Database.")
else:
    try:
        client = MongoClient(mongo_uri, serverSelectionTimeoutMS=3000)
        client.server_info()
        db = client.smartseed_db
    except Exception as e:
        print("[INFO] Local MongoDB connection failed. Falling back to in-memory mongomock database...")
        import mongomock
        client = mongomock.MongoClient()
        db = client.smartseed_db



# 1. Create Admin User (admin@smartseed.com / admin123)
admin_pw = bcrypt.hashpw(b"admin123", bcrypt.gensalt())
db.admins.update_one(
    {"email": "admin@smartseed.com"},
    {"$set": {
        "name": "Super Admin",
        "email": "admin@smartseed.com",
        "password_hash": admin_pw
    }},
    upsert=True
)

# 2. Create Farmer User (farmer@smartseed.com / farmer123)
farmer_pw = bcrypt.hashpw(b"farmer123", bcrypt.gensalt())
user_doc = db.users.find_one({"email": "farmer@smartseed.com"})
if not user_doc:
    res = db.users.insert_one({
        "name": "Sunil Perera",
        "email": "farmer@smartseed.com",
        "password_hash": farmer_pw,
        "created_at": datetime.utcnow()
    })
    user_id = res.inserted_id
else:
    user_id = user_doc["_id"]

# 3. Create Sample Farm
farm_doc = db.farms.find_one({"user_id": user_id})
if not farm_doc:
    res_farm = db.farms.insert_one({
        "user_id": user_id,
        "farm_name": "Green Valley Estate",
        "location": {
            "lat": 6.9271,
            "lng": 79.8612,
            "district": "Colombo",
            "zone": "Wet Zone"
        },
        "agro_zone": "WL1",
        "altitude": 25.0,
        "sensors": {
            "device_id": "DEV_001"
        },
        "crop_type": "Rice"
    })
    farm_id = res_farm.inserted_id
else:
    farm_id = farm_doc["_id"]

# 4. Insert Initial Live Sensor Reading
db.sensor_readings.insert_one({
    "device_id": "DEV_001",
    "farm_id": farm_id,
    "timestamp": datetime.utcnow(),
    "soil_moisture": 55.0,
    "ph_level": 6.5,
    "temperature": 24.5,
    "nitrogen": 90.0,
    "phosphorus": 42.0,
    "potassium": 43.0,
    "predicted_soil": "Noncalcic Brown soils",
    "confidence": 94.2
})

print("=" * 60)
print("DEMO DATA SEEDED SUCCESSFULLY!")
print("Admin Login  : admin@smartseed.com  | Password: admin123")
print("Farmer Login : farmer@smartseed.com | Password: farmer123")
print("Sample Farm  : Green Valley Estate (Device ID: DEV_001)")
print("=" * 60)
