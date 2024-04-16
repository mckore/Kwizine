from pydantic import BaseModel, Field, EmailStr, validator, GetJsonSchemaHandler, GetCoreSchemaHandler, ConfigDict, TypeAdapter
from typing import Annotated, Any, Callable
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic_core import core_schema
from typing import Any, Dict, Optional
from pydantic.json_schema import JsonSchemaValue
from typing_extensions import TypedDict, Literal



class PyObjectId(ObjectId):
    @classmethod
    def __get_pydantic_core_schema__(
            cls, _source_type: Any, _handler: Any
    ) -> core_schema.CoreSchema:
        return core_schema.json_or_python_schema(
            json_schema=core_schema.str_schema(),
            python_schema=core_schema.union_schema([
                core_schema.is_instance_schema(ObjectId),
                core_schema.chain_schema([
                    core_schema.str_schema(),
                    core_schema.no_info_plain_validator_function(cls.validate),
                ])
            ]),
            serialization=core_schema.plain_serializer_function_ser_schema(
                lambda x: str(x)
            ),
        )

    @classmethod
    def validate(cls, value) -> ObjectId:
        if not ObjectId.is_valid(value):
            raise ValueError("Invalid ObjectId")
        return ObjectId(value)


class MongoBaseModel(BaseModel):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        json_encoders = {ObjectId: str}

class IngredientBase(BaseModel):
    unit: str
    size: int
    temperature: List[str]
    subtype: List[str]

class IngredientAttributes(BaseModel):
    __root__: Optional[Dict[str, IngredientBase]]

class RecipeBase(MongoBaseModel):
    title: str = Field(..., min_length=3)
    ingredients: Optional[IngredientAttributes]
    cuisine_origin: Optional[str]
    cuisine_profile: List[Literal['sweet', 'sour', 'salty', 'bitter', 'umami', 'savory']]

class RecipeUpdate(MongoBaseModel):
    ingredients: Optional[str] = None
    cuisine_origin: Optional[str] = None

class MorceauDB(RecipeBase):
    pass

# item = {"brand": "Longchamp", "size": 32, "year": 2024, "style": "portefeuille", "apparel_type": "handbag", "price": 700}

# item = {"price": 700}

# cdb = ItemUpdate(**item)

# print(jsonable_encoder(cdb))