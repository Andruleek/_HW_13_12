from fastapi import FastAPI, Request, Depends, HTTPException, status
from src.routes import contacts
from sqlalchemy.ext.asyncio import AsyncSession
from fastapi_limiter import FastAPILimiter
from fastapi_limiter.depends import RateLimiter
from datetime import datetime  
from sqlalchemy import text
from sqlalchemy.orm import Session
from src.database.db import get_db
import cloudinary
from src.conf.config import CLOUDINARY_CLOUD_NAME, CLOUDINARY_API_KEY, CLOUDINARY_API_SECRET
from src.routes.contacts import router as contacts_router

app = FastAPI()

app.include_router(contacts.router, prefix="/api")

add_cors_middleware(
    app,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

cloudinary.config(
    cloud_name=CLOUDINARY_CLOUD_NAME,
    api_key=CLOUDINARY_API_KEY,
    api_secret=CLOUDINARY_API_SECRET
)


@app.get("/", tags=["Root"])
async def root():
    return {"message": "Hello FastApi"}


@app.get("/api/healthchecker")
async def healthchecker(db: AsyncSession = Depends(get_db)):
    try:
        # Make request
        result = await db.execute(text("SELECT 1"))
        result = result.fetchone()
        if result is None:
            raise HTTPException(status_code=500, detail="Database is not configured correctly")
        return {"message": "Welcome to FastAPI!"}
    except Exception as e:
        print(e)
        raise HTTPException(status_code=500, detail="Error connecting to the database")


@app.on_event("startup")
async def startup():
    await FastAPILimiter.init(redis_connection_url="redis://localhost:6379")

@app.get("/contacts", dependencies=[Depends(RateLimiter(times=10, seconds=60))])
async def get_contacts():
    # Код для отримання контактів
    pass

@app.post("/contacts", dependencies=[Depends(RateLimiter(times=5, seconds=60))])
async def create_contact():
    # Код для створення контакту
    pass


