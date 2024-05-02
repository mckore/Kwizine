from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from bson import ObjectId
from backend.settings.models import RecipeBase, MorceauDB, RecipeUpdate
from typing import Dict, Optional, List
from backend.settings.dbsettings import DB_COLLECTION
from loguru import logger


RESULTS_PER_PAGE = 25
logger.info("Loading router...")
# change references to entities

router = APIRouter()

@router.get("/", response_description="List all items")
async def list_items(request:Request, title:Optional[str]=None, page:int=1)-> List[MorceauDB]:
    try:
        skip = (page-1)*RESULTS_PER_PAGE
        full_query = request.app.mongodb[DB_COLLECTION].find().sort("_id", 1).skip(skip).limit(RESULTS_PER_PAGE)
        results = [MorceauDB(**raw_item) async for raw_item in full_query]
        return results
    except Exception as e:
        logger.exception("Error listing items", title, page)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error listing items") from e

@router.get("/all", response_description="List all items")
async def list_items(request:Request)-> List[MorceauDB]:
    try:
        full_query = request.app.mongodb[DB_COLLECTION].find().sort("_id", 1)
        results = [MorceauDB(**raw_item) async for raw_item in full_query]
        return results
    except Exception as e:
        logger.exception("Error listing items")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error listing items") from e

@router.post("/", response_description="Create new item")
async def create_item(request: Request, item: RecipeBase = Body(...)):
    try:
        item = jsonable_encoder(item)
        new_item = await request.app.mongodb[DB_COLLECTION].insert_one(item)
        created_item = await request.app.mongodb[DB_COLLECTION].find_one(
        {"_id": new_item.inserted_id}
        )
        return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_item)
    except Exception as e:
        logger.exception("Error creating item", item)
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail="Error creating item") from e

@router.get("/{id}", response_description="Get an item by id")
async def show_item_id(id:str, request: Request):
    try:
        if(item:= await request.app.mongodb[DB_COLLECTION].find_one({"_id": ObjectId(id)})) is not None:
            logger.info(f"request for {id}!")
            return MorceauDB(**item)
    except Exception as e:
        logger.exception(f"Error getting item {id}")
        raise HTTPException(status_code=status.HTTP_500_INTERNAL_SERVER_ERROR, detail=f"Error getting item {id}") from e

@router.get("/{title})", response_description="Get an item by id")
async def show_item_id(title:str, request: Request):
    if(item:= await request.app.mongodb[DB_COLLECTION].find_one({"title": title})) is not None:
        return MorceauDB(**item)
    raise HTTPException(status_code=404, detail=f"Item {id} not found")

@router.patch("/{id}", response_description="Update an item by id")
async def update_item(request: Request, id:str, item: RecipeUpdate = Body(...)):
    await request.app.mongodb[DB_COLLECTION].update_one({"_id": id},{"$set": item.model_dump(exclude_unset=True)})
    if (item:= await request.app.mongodb[DB_COLLECTION].find_one({"_id": ObjectId(id)})) is not None:
        return MorceauDB(**item)
    raise HTTPException(status_code=404, detail=f"Item {id} not found")

@router.delete("/{id}", response_description="Delete an item by id")
async def delete_item(request: Request, id:str):
    delete_result = await request.app.mongodb[DB_COLLECTION].delete_one({"_id": id}) 
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    raise HTTPException(status_code=404, detail=f"Item {id} not found")