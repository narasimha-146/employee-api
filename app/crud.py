# app/crud.py
from datetime import datetime, timedelta
from typing import List, Optional, Dict, Any

from jose import jwt, JWTError
from passlib.context import CryptContext
from fastapi import HTTPException, status, Depends
from fastapi.security import OAuth2PasswordBearer

from .database import db

import os

SECRET_KEY = os.getenv("SECRET_KEY", "please-change-me")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 30))

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

# Collections
users_collection = db["users"]
employees_collection = db["employees"]


# ---------------------------
# Password utils
# ---------------------------
def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


# ---------------------------
# JWT utils
# ---------------------------
def create_access_token(data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
    to_encode = data.copy()
    expire = datetime.utcnow() + (expires_delta or timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES))
    to_encode.update({"exp": expire})
    token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return token


def decode_access_token(token: str) -> dict:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid or expired token")


async def get_current_user(token: str = Depends(oauth2_scheme)):
    payload = decode_access_token(token)
    username: str = payload.get("sub")
    if not username:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid token payload")
    user = await users_collection.find_one({"username": username})
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    # remove hashed_password before returning (if needed)
    user.pop("hashed_password", None)
    return user


# ---------------------------
# Employee CRUD + helpers
# ---------------------------
def serialize_employee(emp: dict) -> dict:
    if not emp:
        return None
    return {
        "id": str(emp.get("_id")),
        "employee_id": emp.get("employee_id"),
        "name": emp.get("name"),
        "department": emp.get("department"),
        "salary": emp.get("salary"),
        "joining_date": emp.get("joining_date"),
        "skills": emp.get("skills", []),
    }


async def create_employee(record: dict) -> dict:
    """
    record must be dict with fields validated by Pydantic first.
    Store joining_date as ISO string (YYYY-MM-DD).
    """
    # ensure joining_date is a string (pydantic gives date object sometimes)
    if "joining_date" in record:
        record["joining_date"] = str(record["joining_date"])
    result = await employees_collection.insert_one(record)
    inserted = await employees_collection.find_one({"_id": result.inserted_id})
    return serialize_employee(inserted)


async def get_employees(page: int = 1, page_size: int = 10) -> dict:
    """
    Returns paginated list and metadata.
    """
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10

    skip = (page - 1) * page_size
    cursor = employees_collection.find().skip(skip).limit(page_size)
    items = []
    async for doc in cursor:
        items.append(serialize_employee(doc))

    total = await employees_collection.count_documents({})
    return {
        "page": page,
        "page_size": page_size,
        "total": total,
        "items": items
    }


async def get_employee_by_employee_id(emp_id: str) -> Optional[dict]:
    doc = await employees_collection.find_one({"employee_id": emp_id})
    return serialize_employee(doc)


async def update_employee(emp_id: str, update_data: dict) -> Optional[dict]:
    if "joining_date" in update_data:
        update_data["joining_date"] = str(update_data["joining_date"])
    result = await employees_collection.update_one({"employee_id": emp_id}, {"$set": update_data})
    if result.matched_count == 0:
        return None
    updated = await employees_collection.find_one({"employee_id": emp_id})
    return serialize_employee(updated)


async def delete_employee(emp_id: str) -> bool:
    result = await employees_collection.delete_one({"employee_id": emp_id})
    return result.deleted_count == 1


# ---------------------------
# Query helpers
# ---------------------------
async def get_by_department(department: str, page: int = 1, page_size: int = 10) -> dict:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    skip = (page - 1) * page_size
    cursor = employees_collection.find({"department": department}).skip(skip).limit(page_size)
    items = []
    async for doc in cursor:
        items.append(serialize_employee(doc))
    total = await employees_collection.count_documents({"department": department})
    return {"page": page, "page_size": page_size, "total": total, "items": items}


async def get_by_skill(skill: str, page: int = 1, page_size: int = 10) -> dict:
    if page < 1:
        page = 1
    if page_size < 1:
        page_size = 10
    skip = (page - 1) * page_size
    cursor = employees_collection.find({"skills": {"$in": [skill]}}).skip(skip).limit(page_size)
    items = []
    async for doc in cursor:
        items.append(serialize_employee(doc))
    total = await employees_collection.count_documents({"skills": {"$in": [skill]}})
    return {"page": page, "page_size": page_size, "total": total, "items": items}


async def avg_salary_by_department(department: str) -> Optional[dict]:
    pipeline = [
        {"$match": {"department": department}},
        {"$group": {"_id": "$department", "averageSalary": {"$avg": "$salary"}, "count": {"$sum": 1}}}
    ]
    cursor = employees_collection.aggregate(pipeline)
    results = await cursor.to_list(length=1)
    if not results:
        return None
    r = results[0]
    return {"department": r["_id"], "averageSalary": r["averageSalary"], "count": r["count"]}
