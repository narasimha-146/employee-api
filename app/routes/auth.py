# app/routes/auth.py
from fastapi import APIRouter, HTTPException, status, Depends
from fastapi.security import OAuth2PasswordRequestForm
from datetime import timedelta

from ..models import UserCreate, Token
from ..crud import users_collection, get_password_hash, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/signup", status_code=201)
async def signup(user: UserCreate):
    # check username uniqueness (index exists)
    existing = await users_collection.find_one({"username": user.username})
    if existing:
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed = get_password_hash(user.password)
    doc = {"username": user.username, "email": user.email, "hashed_password": hashed}
    await users_collection.insert_one(doc)
    return {"message": "User created successfully"}


@router.post("/login", response_model=Token)
async def login(form_data: OAuth2PasswordRequestForm = Depends()):
    user = await users_collection.find_one({"username": form_data.username})
    if not user or not verify_password(form_data.password, user["hashed_password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid credentials")

    access_token_expires = timedelta(minutes=30)
    token = create_access_token(data={"sub": user["username"]}, expires_delta=access_token_expires)
    return {"access_token": token, "token_type": "bearer"}
