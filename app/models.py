# app/models.py
from pydantic import BaseModel, Field, EmailStr
from typing import List, Optional
from datetime import date


# ---------------------------
# User models
# ---------------------------
class UserCreate(BaseModel):
    username: str = Field(..., example="alice123")
    email: EmailStr = Field(..., example="alice@example.com")
    password: str = Field(..., example="securepassword")


class Token(BaseModel):
    access_token: str
    token_type: str


# ---------------------------
# Employee models
# ---------------------------
class EmployeeBase(BaseModel):
    employee_id: str = Field(..., example="E002")
    name: str = Field(..., example="Bob")
    department: str = Field(..., example="Engineering")
    salary: float = Field(..., example=70000)
    joining_date: date = Field(..., example="2022-11-20")
    skills: List[str] = Field(..., example=["Java", "MongoDB"])

    class Config:
        schema_extra = {
            "example": {
                "employee_id": "E002",
                "name": "Bob",
                "department": "Engineering",
                "salary": 70000,
                "joining_date": "2022-11-20",
                "skills": ["Java", "MongoDB"]
            }
        }


class EmployeeCreate(EmployeeBase):
    pass


class Employee(EmployeeBase):
    id: Optional[str] = Field(None, example="650f8f2a3a2b1c1234567890")
