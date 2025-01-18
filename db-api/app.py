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

from sabores import router as compounds_router
from ingredientes import router as ingredientes_router
from recetas import router as recetas_router
#from mapeos import router as mapeos_router
#from auth import router as auth_router
from auth import router as auth_router
from dietas import router as dietas_router
from emisiones import router as emisiones_router


app = FastAPI(
    title="API para consulta en la base de datos de FoodDB",
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=[
        "https://food-db-chi.vercel.app",  
    ],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"message": "Welcome to the API"}

# ---------------------------------------------------- INGREDIENTES ---------------------------------------------------- #

# Todos los ingredientes
app.include_router(ingredientes_router, prefix="/ingredientes", tags=["Ingredientes"])

# ---------------------------------------------------- RECETAS ---------------------------------------------------- #

# Todas las recetas
app.include_router(recetas_router, prefix="/recetas", tags=["Recetas"])

# ---------------------------------------------------- COMPOUNDS ---------------------------------------------------- #

app.include_router(compounds_router, prefix="/sabores", tags=["Sabores"])


# ---------------------------------------------------- MAPEO ---------------------------------------------------- #

#app.include_router(mapeos_router, prefix="/mapeo", tags=["Mapeos"])

# ---------------------------------------------------- AUTENTICACIÓN ---------------------------------------------------- #

app.include_router(auth_router, prefix="/auth", tags=["Autenticación"])

 # ---------------------------------------------------- DIETAS ---------------------------------------------------- #

app.include_router(dietas_router, prefix="/dietas", tags=["Dietas"])

# ---------------------------------------------------- EMISIONES ---------------------------------------------------- #

app.include_router(emisiones_router, prefix="/emisiones", tags=["Emisiones"])