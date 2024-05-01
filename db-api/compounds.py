from fastapi import APIRouter, HTTPException
from bson import ObjectId
from typing import List
from pydantic import BaseModel

from models import CompoundModel, CompoundCollection, IngredientCollection
from bd import compounds_collection, ingredientes_collection   # Importa la colección de sabores desde bd.py

router = APIRouter()

@router.get(
    "/",
    response_description="Listar todos los compuestos",
    response_model=CompoundCollection,
    response_model_by_alias=False,
)
async def list_compounds():
    """
    Listar todos los compuestos.
    """
    return CompoundCollection(compounds=await compounds_collection.find().to_list(1000))


@router.get(
    "/ingredientes/{sabor}",
    response_description="Buscar ingredientes por sabor",
    response_model=IngredientCollection,
    response_model_by_alias=False,
)
async def buscar_ingredientes_por_sabor(sabor: str):
    """
    Buscar ingredientes por sabor.
    """
    # Buscar ingredientes que contengan el sabor en su lista de compuestos
    cursor = ingredientes_collection.find({"compounds.ingredient": sabor})

    # Convertir el cursor a una lista de ingredientes
    ingredientes = await cursor.to_list(length=1000)

    if ingredientes:
        return IngredientCollection(ingredientes=ingredientes)
    else:
        raise HTTPException(status_code=404, detail=f"No se encontraron ingredientes con el sabor {sabor}")
