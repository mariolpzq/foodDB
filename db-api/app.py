import os
from typing import Optional, List, Union

from fastapi import FastAPI, Body, HTTPException, status
from fastapi.middleware.cors import CORSMiddleware
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
from sabores import router as compounds_router
from ingredientes import router as ingredientes_router
from recetas import router as recetas_router
from mapeos import router as mapeos_router
#from auth import router as auth_router
from auth import router as auth_router
from dietas import router as dietas_router


app = FastAPI(
    title="API para consulta en la base de datos de FoodDB",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], 
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------- INGREDIENTES ---------------------------------------------------- #

# Todos los ingredientes
app.include_router(ingredientes_router, prefix="/ingredientes", tags=["Ingredientes"])

# ---------------------------------------------------- RECETAS ---------------------------------------------------- #

# Todas las recetas
app.include_router(recetas_router, prefix="/recetas", tags=["Recetas"])

# ---------------------------------------------------- BEDCA ---------------------------------------------------- #

# Monta el enrutador de BEDCA
app.include_router(bedca_router, prefix="/bedca", tags=["BEDCA"])

# ---------------------------------------------- RECETAS DE LA ABUELA ---------------------------------------------- #

app.include_router(abuela_router, prefix="/abuela", tags=["Recetas de la Abuela"])

# ---------------------------------------------------- COMPOUNDS ---------------------------------------------------- #

app.include_router(compounds_router, prefix="/sabores", tags=["Sabores"])


# ---------------------------------------------------- MAPEO ---------------------------------------------------- #

app.include_router(mapeos_router, prefix="/mapeo", tags=["Mapeos"])

# ---------------------------------------------------- AUTENTICACIÓN ---------------------------------------------------- #

app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])

 # ---------------------------------------------------- DIETAS ---------------------------------------------------- #

app.include_router(dietas_router, prefix="/dietas", tags=["Dietas"])