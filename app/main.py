# app/main.py
from fastapi import FastAPI
from .routes import auth, employees
from .database import init_db

app = FastAPI(title="Employee API with JWT Auth & Validation")

# include routers
app.include_router(auth.router)
app.include_router(employees.router)


@app.on_event("startup")
async def on_startup():
    # create collections, validators, and indexes
    await init_db()
