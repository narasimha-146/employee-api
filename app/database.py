# app/database.py
import os
from dotenv import load_dotenv
from motor.motor_asyncio import AsyncIOMotorClient

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI")
DATABASE_NAME = os.getenv("DATABASE_NAME", "assessment_db")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DATABASE_NAME]


async def init_db():
    """
    Ensure collections exist with JSON Schema validators and required indexes.
    Called at application startup.
    """
    # ---------------------------
    # Employees JSON Schema
    # ---------------------------
    employees_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["employee_id", "name", "department", "salary", "joining_date", "skills"],
            "properties": {
                "employee_id": {"bsonType": "string", "description": "unique employee id"},
                "name": {"bsonType": "string"},
                "department": {"bsonType": "string"},
                "salary": {"bsonType": ["double", "int"]},
                "joining_date": {"bsonType": "string", "description": "ISO date string YYYY-MM-DD"},
                "skills": {
                    "bsonType": "array",
                    "items": {"bsonType": "string"}
                }
            }
        }
    }

    # ---------------------------
    # Users JSON Schema
    # ---------------------------
    users_validator = {
        "$jsonSchema": {
            "bsonType": "object",
            "required": ["username", "email", "hashed_password"],
            "properties": {
                "username": {"bsonType": "string"},
                "email": {"bsonType": "string"},
                "hashed_password": {"bsonType": "string"}
            }
        }
    }

    existing = await db.list_collection_names()

    # Create or modify employees collection with validator
    if "employees" not in existing:
        await db.create_collection("employees", validator=employees_validator)
    else:
        try:
            await db.command({
                "collMod": "employees",
                "validator": employees_validator,
                "validationLevel": "moderate"
            })
        except Exception:
            # ignore if collMod fails on some older server versions
            pass

    # Create or modify users collection with validator
    if "users" not in existing:
        await db.create_collection("users", validator=users_validator)
    else:
        try:
            await db.command({
                "collMod": "users",
                "validator": users_validator,
                "validationLevel": "moderate"
            })
        except Exception:
            pass

    # ---------------------------
    # Indexes
    # ---------------------------
    # Unique index on employee_id
    try:
        await db["employees"].create_index("employee_id", unique=True)
    except Exception:
        pass

    # Unique index on username
    try:
        await db["users"].create_index("username", unique=True)
    except Exception:
        pass
