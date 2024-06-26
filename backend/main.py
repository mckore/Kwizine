from dbsettings import DB_URL, DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, APIRouter, Request, Body, status
from routers.items import router as items_router

app = FastAPI()
app.include_router(items_router, prefix="/items", tags=["items"])

@app.on_event("startup")

async def startup_db_client():
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    app.mongodb_client.close()


@app.get("/health")
async def health():
    return {"message: healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)