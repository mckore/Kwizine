from backend.settings.dbsettings import DB_URL, DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, APIRouter, Request, Body, status
from routers.items import router as items_router
from loguru import logger

# setup loggers

app = FastAPI()
app.include_router(items_router, prefix="/recipes", tags=["recipes"])

@app.on_event("startup")

async def startup_db_client():
    logger.info("Starting DB connection...")
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Closing connection to DB...")
    app.mongodb_client.close()

@app.get("/health")
async def health():
    logger.info("Health check")
    return {"message: healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)