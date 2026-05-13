import bcrypt
from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()
client = MongoClient(os.getenv('MONGO_URI'))
db = client.smartseed_db

password = b"admin123"
hashed = bcrypt.hashpw(password, bcrypt.gensalt())

db.admins.insert_one({
    "name": "Super Admin",
    "email": "admin@smartseed.com",
    "password_hash": hashed
})
print("Admin user created successfully!")