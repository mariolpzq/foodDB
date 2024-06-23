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

from models import EmissionModel, EmissionCollection
from bd import get_collection, emissions_collection

from fastapi import Depends
from auth import get_current_user, UserModel

import json

router = APIRouter()


@router.get("/", response_model=EmissionCollection)
async def get_emisiones():

    emisiones = await emissions_collection.find().to_list(None)

    return EmissionCollection(emissions=emisiones)


@router.get("/{id}", response_model=EmissionModel)
async def get_emision(id: str):

    emision = await emissions_collection.find_one({"_id": ObjectId(id)})

    if emision is None:
        raise HTTPException(status_code=404, detail="Emission not found")

    return EmissionModel(**emision)