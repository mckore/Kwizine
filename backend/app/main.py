from backend.settings.dbsettings import DB_URL, DB_NAME
from motor.motor_asyncio import AsyncIOMotorClient
from fastapi import FastAPI, APIRouter, Request, Body, status
from routers.items import router as items_router
import logging
from backend.settings.services import EchoService
import random
import time
import string

# setup loggers
logging.config.fileConfig('../logging.conf', disable_existing_loggers=False)

logger = logging.getLogger(__name__)

app = FastAPI()
app.include_router(items_router, prefix="/recipes", tags=["recipes"])

@app.on_event("startup")

async def startup_db_client():
    logger.info("Connecting to database...")
    app.mongodb_client = AsyncIOMotorClient(DB_URL)
    app.mongodb = app.mongodb_client[DB_NAME]

@app.on_event("shutdown")
async def shutdown_db_client():
    logger.info("Closing connection to database...")
    app.mongodb_client.close()


@app.middleware("http")
async def log_requests(request: Request, call_next):
    idem = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
    logger.info(f"rid={idem} start request path={request.url.path}")
    start_time = time.time()
    
    response = await call_next(request)
    
    process_time = (time.time() - start_time) * 1000
    formatted_process_time = '{0:.2f}'.format(process_time)
    logger.info(f"rid={idem} completed_in={formatted_process_time}ms status_code={response.status_code}")
    
    return response

@app.get("/health")
async def health():
    logger.info("Health check")
    EchoService().echo(msg="Service Healthy")
    return {"message: healthy"}


if __name__ == "__main__":
    uvicorn.run("main:app", reload=True)