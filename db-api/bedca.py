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
from bd import bedca_collection

router = APIRouter()


# ---------------------------------------------------- BEDCA ---------------------------------------------------- #


@router.get(
    "/",
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
    "/{nombre}",
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

