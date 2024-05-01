import os
from typing import Optional, List, Union

from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
from bson import ObjectId

from models import IngredientModel, IngredientCollection
from bd import ingredientes_collection

router = APIRouter()

@router.get(
    "/",
    response_description="Listar todos los ingredientes",
    response_model=IngredientCollection,
    response_model_by_alias=False,
)
async def list_ingredientes():
    """
    Listar todos los ingredientes.
    """
    return IngredientCollection(ingredientes=await ingredientes_collection.find().to_list(2000))


