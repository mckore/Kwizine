from fastapi import APIRouter, Request, Body, status, HTTPException, Depends
from fastapi.encoders import jsonable_encoder
from fastapi.responses import JSONResponse
from models import ItemBase, HauteDB, ItemUpdate
from typing import Dict, Optional, List
from dbsettings import DB_COLLECTION

RESULTS_PER_PAGE = 25


router = APIRouter()

@router.get("/", response_description="List all items")
async def list_items(request:Request, min_price: int=50, max_price: int=100000, brand:Optional[str]=None, page:int=1)-> List[HauteDB]:
    skip = (page-1)*RESULTS_PER_PAGE
    query = {"price":{"$lt": max_price, "$gt": min_price}}
    if brand:
        query["brand"] = brand

    full_query = request.app.mongodb[DB_COLLECTION].find(query).sort("_id", 1).skip(skip).limit(RESULTS_PER_PAGE)
    results = [HauteDB(**raw_item) async for raw_item in full_query]
    return results

@router.get("/all", response_description="List all items")
async def list_items(request:Request)-> List[HauteDB]:
    full_query = request.app.mongodb[DB_COLLECTION].find().sort("_id", 1)
    results = [HauteDB(**raw_item) async for raw_item in full_query]
    return results

@router.post("/", response_description="Create new item")
async def create_item(request: Request, item: ItemBase = Body(...)):
    item = jsonable_encoder(item)
    new_item = await request.app.mongodb[DB_COLLECTION].insert_one(item)
    created_item = await request.app.mongodb[DB_COLLECTION].find_one(
        {"_id": new_item.inserted_id}
    )
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_item)

@router.get("/{id}", response_description="Get an item by id")
async def show_item_id(id:str, request: Request):
    if(item:= await request.app.mongodb[DB_COLLECTION].find_one({"_id": id})) is not None:
        return HauteDB(**item)
    raise HTTPException(status_code=404, detail=f"Item {id} not found")

@router.patch("/{id}", response_description="Update an item by id")
async def update_item(request: Request, id:str, item: ItemUpdate = Body(...)):
    await request.app.mongodb[DB_COLLECTION].update_one({"_id": id},{"$set": item.model_dump(exclude_unset=True)})
    if (item:= await request.app.mongodb[DB_COLLECTION].find_one({"_id": id})) is not None:
        return HauteDB(**item)
    raise HTTPException(status_code=404, detail=f"Item {id} not found")

@router.delete("/{id}", response_description="Delete an item by id")
async def delete_item(request: Request, id:str):
    delete_result = await request.app.mongodb[DB_COLLECTION].delete_one({"_id": id}) 
    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT, content=None)
    raise HTTPException(status_code=404, detail=f"Item {id} not found")