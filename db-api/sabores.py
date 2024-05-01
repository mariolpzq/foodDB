from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from pydantic import BaseModel

from models import CompoundModel, CompoundCollection, IngredientCollection
from bd import compounds_collection, ingredientes_collection   # Importa la colección de sabores desde bd.py

router = APIRouter()

@router.get(
    "/",
    response_description="Listar todos los sabores",
    response_model=CompoundCollection,
    response_model_by_alias=False,
)
async def listar_sabores():
    """
    Listar todos los compuestos.
    """
    return CompoundCollection(compounds=await compounds_collection.find().to_list(1000))



