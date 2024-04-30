from pydantic import BaseModel, Field, EmailStr, validator, GetJsonSchemaHandler, GetCoreSchemaHandler, ConfigDict, TypeAdapter, RootModel
from typing import Annotated, Any, Callable
from fastapi.encoders import jsonable_encoder
from pydantic_core import core_schema
from typing import Any, Dict, Optional, List
from pydantic.json_schema import JsonSchemaValue
from typing_extensions import TypedDict, Literal
from pydantic.functional_validators import BeforeValidator

PyObjectId = Annotated[str, BeforeValidator(str)]

class IngredientBase(BaseModel):
    unit: str
    size: int
    temperature: List[str]
    subtype: List[str]

class IngredientAttributes(RootModel):
    root: Optional[Dict[str, IngredientBase]]

class RecipeBase(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: str = Field(..., min_length=3)
    ingredients: Optional[IngredientAttributes] = None
    cuisine_origin: Optional[str] = None
    cuisine_profile: Optional[List[Literal["sweet", "savory", "sour", "bitter", "umami"]]] = None

class RecipeUpdate(BaseModel):
    ingredients: Optional[str] = None
    cuisine_origin: Optional[str] = None
    cuisine_profile: Optional[List[str]] = None

class MorceauDB(RecipeBase):
    pass