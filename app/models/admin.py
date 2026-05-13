from app import mongo

class Admin:
    @staticmethod
    def get_admin_by_email(email):
        return mongo.db.admins.find_one({"email": email})