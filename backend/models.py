from pydantic import BaseModel, Field, EmailStr, validator, GetJsonSchemaHandler, GetCoreSchemaHandler, ConfigDict
from typing import Annotated, Any, Callable
from bson import ObjectId
from fastapi.encoders import jsonable_encoder
from pydantic_core import core_schema
from typing import Any, Dict, Optional
from pydantic.json_schema import JsonSchemaValue

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

class ItemBase(MongoBaseModel):
    brand: str = Field(..., min_length=3)
    size: int = Field()
    year: int = Field(gt=1990, lt=2050)
    style: str = Field(...,min_length=3)
    apparel_type: str = Field(..., min_length=3)
    price: int = Field(gt=0)

class ItemUpdate(MongoBaseModel):
    price: Optional[int] = None
class HauteDB(ItemBase):
    pass

# item = {"brand": "Longchamp", "size": 32, "year": 2024, "style": "portefeuille", "apparel_type": "handbag", "price": 700}

# item = {"price": 700}

# cdb = ItemUpdate(**item)

# print(jsonable_encoder(cdb))