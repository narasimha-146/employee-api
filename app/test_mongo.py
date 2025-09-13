# app/test_mongo.py
import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()  # load environment variables from .env

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "assessment_db")

print("Connecting to MongoDB...")

client = MongoClient(MONGO_URI)
db = client[DATABASE_NAME]

# Sample query for testing
employee = db.employees.find_one()
print("First employee in DB:", employee)
