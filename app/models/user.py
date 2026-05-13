from app import mongo
from bson.objectid import ObjectId

class User:
    @staticmethod
    def create_user(name, email, password_hash, created_by_admin_id):
        user_data = {
            "name": name,
            "email": email,
            "password_hash": password_hash,
            "created_by": ObjectId(created_by_admin_id)
        }
        return mongo.db.users.insert_one(user_data).inserted_id

    @staticmethod
    def get_user_by_email(email):
        return mongo.db.users.find_one({"email": email})