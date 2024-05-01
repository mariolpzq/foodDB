import os
from typing import Optional, List, Union

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
from bson import ObjectId

from bedca import router as bedca_router  # Importa el enrutador de BEDCA
from abuela import router as abuela_router 
from compounds import router as compounds_router
from ingredientes import router as ingredientes_router


app = FastAPI(
    title="API para consulta en la base de datos de FoodDB",
)

# ---------------------------------------------------- INGREDIENTES ---------------------------------------------------- #

# Todos los ingredientes
app.include_router(ingredientes_router, prefix="/ingredientes", tags=["Ingredientes"])

# ---------------------------------------------------- BEDCA ---------------------------------------------------- #

# Monta el enrutador de BEDCA
app.include_router(bedca_router, prefix="/bedca", tags=["BEDCA"])

# ---------------------------------------------- RECETAS DE LA ABUELA ---------------------------------------------- #

app.include_router(abuela_router, prefix="/abuela", tags=["Recetas de la Abuela"])

# ---------------------------------------------------- COMPOUNDS ---------------------------------------------------- #

app.include_router(compounds_router, prefix="/compounds", tags=["Compuestos"])