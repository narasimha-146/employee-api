# app/routes/employees.py
from fastapi import APIRouter, Depends, HTTPException, Query
from typing import Optional

from ..models import EmployeeCreate, Employee
from ..crud import (
    get_current_user,
    create_employee,
    get_employees,
    get_employee_by_employee_id,
    update_employee,
    delete_employee,
    get_by_department,
    get_by_skill,
    avg_salary_by_department,
)
from ..database import db

router = APIRouter(prefix="/employees", tags=["Employees"])


@router.post("/", response_model=dict)
async def post_employee(payload: EmployeeCreate, current_user: dict = Depends(get_current_user)):
    # create employee record
    doc = payload.dict()
    created = await create_employee(doc)
    return {"message": "Employee created", "employee": created}


@router.get("/", response_model=dict)
async def list_employees(
    page: int = Query(1, ge=1, description="Page number"),
    page_size: int = Query(10, ge=1, le=100, description="Items per page"),
    current_user: dict = Depends(get_current_user),
):
    return await get_employees(page=page, page_size=page_size)


@router.get("/{employee_id}", response_model=dict)
async def get_employee(employee_id: str, current_user: dict = Depends(get_current_user)):
    emp = await get_employee_by_employee_id(employee_id)
    if not emp:
        raise HTTPException(status_code=404, detail="Employee not found")
    return emp


@router.put("/{employee_id}", response_model=dict)
async def put_employee(employee_id: str, updates: dict, current_user: dict = Depends(get_current_user)):
    updated = await update_employee(employee_id, updates)
    if not updated:
        raise HTTPException(status_code=404, detail="Employee not found or no changes")
    return {"message": "Employee updated", "employee": updated}


@router.delete("/{employee_id}", response_model=dict)
async def remove_employee(employee_id: str, current_user: dict = Depends(get_current_user)):
    ok = await delete_employee(employee_id)
    if not ok:
        raise HTTPException(status_code=404, detail="Employee not found")
    return {"message": "Employee deleted"}


# ---------- extra queries ----------
@router.get("/department/{department}", response_model=dict)
async def employees_by_department(
    department: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    return await get_by_department(department, page=page, page_size=page_size)


@router.get("/skills/{skill}", response_model=dict)
async def employees_by_skill(
    skill: str,
    page: int = Query(1, ge=1),
    page_size: int = Query(10, ge=1, le=100),
    current_user: dict = Depends(get_current_user),
):
    return await get_by_skill(skill, page=page, page_size=page_size)


@router.get("/avg-salary/{department}", response_model=dict)
async def avg_salary(department: str, current_user: dict = Depends(get_current_user)):
    res = await avg_salary_by_department(department)
    if not res:
        raise HTTPException(status_code=404, detail="No employees in this department")
    return res
