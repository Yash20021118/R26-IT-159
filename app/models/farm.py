from app import mongo
from bson.objectid import ObjectId

class Farm:
    @staticmethod
    def create_farm(user_id, farm_name, lat, lng, district, zone, agro_zone, altitude, device_id):
        farm_data = {
            "user_id": ObjectId(user_id),
            "farm_name": farm_name,
            "altitude": altitude, 
            "location": {
                "lat": float(lat),
                "lng": float(lng),
                "district": district,
                "zone": zone,
                "agro_zone": agro_zone 
            },
            "sensors": {
                "device_id": device_id,
                "status": "Active"
            }
        }
        return mongo.db.farms.insert_one(farm_data).inserted_id

    @staticmethod
    def get_farms_by_user(user_id):
        return list(mongo.db.farms.find({"user_id": ObjectId(user_id)}))
    
    @staticmethod
    def get_farm_by_id(farm_id):
        return mongo.db.farms.find_one({"_id": ObjectId(farm_id)})


    @staticmethod
    def get_farm_by_device(device_id):
        return mongo.db.farms.find_one({"sensors.device_id": device_id})