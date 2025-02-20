from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import connect_to_mongo, close_mongo_connection
from .routes import exchanges, coins, pairs, users

app = FastAPI(title="Scanner API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роуты
app.include_router(exchanges.router)
app.include_router(coins.router)
app.include_router(pairs.router)
app.include_router(users.router)

@app.on_event("startup")
async def startup_db_client():
    await connect_to_mongo()

@app.on_event("shutdown")
async def shutdown_db_client():
    await close_mongo_connection()

@app.get("/")
async def root():
    return {"message": "Scanner API is running"}
