from app import mongo
from bson.objectid import ObjectId
import pymongo

class SensorData:
    @staticmethod
    def get_latest_reading(device_id):
        # To get the latest data from the relevant sensor device
        return mongo.db.sensor_readings.find_one(
            {"device_id": device_id},
            sort=[("timestamp", pymongo.DESCENDING)]
        )