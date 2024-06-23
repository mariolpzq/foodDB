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
from bd import ingredientes_collection, bedca_collection

router = APIRouter()

@router.get(
    "/",
    response_description="Listar todos los ingredientes",
    response_model=IngredientCollection,
    response_model_by_alias=False,
)
async def listar_ingredientes():
    """
    Listar todos los ingredientes.
    """
    return IngredientCollection(ingredientes=await ingredientes_collection.find().to_list(2000))

@router.get(
    "/sabor/{sabor}",
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


@router.get(
    "/{ingrediente_id}",
    response_description="Obtener un ingrediente por su ID",
    response_model=IngredientModel,
    response_model_by_alias=False,
)
async def obtener_ingrediente_por_id(ingrediente_id: str):
    """
    Obtener un ingrediente por su ID.
    """
    ingrediente = await ingredientes_collection.find_one({"_id": ObjectId(ingrediente_id)})
    if ingrediente is None:
        raise HTTPException(status_code=404, detail="Ingrediente no encontrado")
    return IngredientModel(**ingrediente)




# ---------------------------------------------------- BEDCA ---------------------------------------------------- #


@router.get(
    "/bedca/",
    response_description="Listar todas las ingredientes de BEDCA",
    response_model=IngredientCollection,
    response_model_by_alias=False,
)
async def listar_bedca():
    """
    Listar todos los ingredientes de BEDCA.

    """
    return IngredientCollection(ingredientes=await bedca_collection.find().to_list(1000))


@router.get(
    "/bedca/{nombre}",
    response_description="Buscar un ingrediente de BEDCA",
    response_model=IngredientCollection,
    response_model_by_alias=False,
)
async def buscar_BEDCA_por_nombre(nombre: str):
    """
    Buscar un ingrediente de BEDCA por su nombre.    
    """
    
    ingredients = []
    for ingredient in await bedca_collection.find().to_list(1000):
        if nombre in ingredient['name_esp'].lower() or nombre in ingredient['name_en'].lower():
            ingredients.append(ingredient)

    print("Ingredientes encontrados: ", len(ingredients))
    if len(ingredients) > 0:
        return IngredientCollection(ingredientes=ingredients)

    raise HTTPException(status_code=404, detail=f"No se encontraron ingredientes con el nombre {nombre}")

