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


app = FastAPI(
    title="API para consulta en la base de datos de FoodDB",
)
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
# print (os.environ["MONGODB_URL"])
db = client.tfg
bedca_collection = db.get_collection("bedca")
abuela_collection = db.get_collection("abuela")

# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]

# ---------------------------------------------------- BEDCA ---------------------------------------------------- #


class BedcaModel(BaseModel): # Se crea el modelo de la receta de BEDCA
    """
    Container para una receta de BEDCA.
    """   
    
    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None) # El alias es para que en la base de datos se guarde como _id
    name_esp : str = Field(...)
    name_en : str = Field(...)
    langual : str = Field(...)
    origin_ISO : str = Field(...)
    source : str = Field(...)
    category_esp : str = Field(...)
    category_en : str = Field(...)
    edible : float = Field(...)
    compounds : List[str] = Field(...)
    nutritional_info_100g : dict = Field(...)
    oms_lights : dict = Field(...)
    
    model_config = ConfigDict( # Configuración del modelo
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "_id": "ObjectID(66261bfd6f790019dbc6b220)",
            "name_esp": "Cerdo, pierna, cruda, con grasa separable",
            "name_en": "Pork, leg, raw, with separable fat",
            "langual": "A0150 A0459 A0633 A0714 A0726 A0737 A0794 B1136 C0269 E0150 F0003 G0001 H0001 J0001 K0003 M0001 N0001 P0024 R0212 R0497 Z0024 Z0112",
            "origin_ISO": "ES",
            "source": "BEDCA",
            "category_esp": "Carne y productos cárnicos",
            "category_en": "Meat and meat products",
            "edible": 75,
            "compounds": [],
            "nutritional_info_100g": {
                "car": 0,
                "energy_kcal": 212.496,
                "energy_kj": 888.233,
                "pro": 19,
                "wat": 65.8,
                "sug": "null",
                "fats": {
                "total_fat": 15.2,
                "sat": 5.1,
                "trans": "null"
                },
                "fiber": 0,
                "cal": 8,
                "chloride": 50,
                "iron": 1.5,
                "pot": 370,
                "mag": 22,
                "sod": 80,
                "salt": 200,
                "phos": 230,
                "cholesterol": 63
            },
            "oms_lights": {
                "salt": "green",
                "sug": "",
                "total_fat": "orange",
                "trans": ""
            },
        }
    )
    
class BedcaCollection(BaseModel):
    """
        A container holding a list of `BedcaModel` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    bedca: List[BedcaModel]

@app.get(
    "/bedca/",
    response_description="Listar todas las ingredientes de BEDCA",
    response_model=BedcaCollection,
    response_model_by_alias=False,
)
async def list_bedca():
    """
    Listar todos los ingredientes de BEDCA.

    """
    return BedcaCollection(bedca=await bedca_collection.find().to_list(1000))


@app.get(
    "/bedca/{nombre}",
    response_description="Buscar un ingrediente de BEDCA",
    response_model=BedcaCollection,
    response_model_by_alias=False,
)
async def search_bedca_esp(nombre: str):
    """
    Buscar un ingrediente de BEDCA por su nombre.    
    """
    
    ingredients = []
    for ingredient in await bedca_collection.find().to_list(1000):
        if nombre in ingredient['name_esp'].lower() or nombre in ingredient['name_en'].lower():
            ingredients.append(ingredient)

    print("Ingredientes encontrados: ", len(ingredients))
    if len(ingredients) > 0:
        return BedcaCollection(bedca=ingredients)

    raise HTTPException(status_code=404, detail=f"No se encontraron ingredientes con el nombre {nombre}")



# ---------------------------------------------- RECETAS DE LA ABUELA ---------------------------------------------- #


"""
documento = {
            "title": row['Nombre'],
            'url': row['URL'],
            'descripcion': row['Contexto'],
            'source': 'Recetas de la abuela',
            'language_ISO': 'ES',
            'origin_ISO' : row['Pais'], # Gastronomía de origen,
            'n_diners': n_diners,
            'dificultad': row['Dificultad'], # Dificultad de la receta
            'category': categoria,
            'subcategory': '',
            'minutes': int(total_minutes),
            'n_ingredients': len(lista_ingredientes),
            'ingredients' : lista_ingredientes,
            'n_steps': len(lista_pasos),
            'steps' : lista_pasos,
            'images': [],
            'interactions': '',
            'aver_rate': aver_rate,
            'num_interactions': num_interactions, # Número de reviews de la receta
            'tags' : [],
            'num_tags': '',
            'dietary_preferences' : dietary_preferences,
        }
"""


class AbuelaModel(BaseModel): # Se crea el modelo de la receta de la abuela
    """
    Container para una receta de la abuela.
    """   
    
    # The primary key for the StudentModel, stored as a `str` on the instance.
    # This will be aliased to `_id` when sent to MongoDB,
    # but provided as `id` in the API requests and responses.
    id: Optional[PyObjectId] = Field(alias="_id", default=None) # El alias es para que en la base de datos se guarde como _id
    title : str = Field(...)
    url : str = Field(...)
    descripcion : str = Field(...)
    source : str = Field(...)
    language_ISO : str = Field(...)
    origin_ISO : str = Field(...)
    n_diners : Union[str,int] = Field(...)
    dificultad : str = Field(...)
    category : List[str] = Field(...)
    subcategory : str = Field(...)
    minutes : int = Field(...)
    n_ingredients : int = Field(...)
    ingredients : List[str] = Field(...)
    n_steps : int = Field(...)
    steps : List[str] = Field(...)
    images : List[str] = Field(...)
    interactions : str = Field(...)
    aver_rate : Union[float,str] = Field(...)
    num_interactions : int = Field(...)
    tags : List[str] = Field(...)
    num_tags : str = Field(...)
    dietary_preferences : List[str] = Field(...)
    
    model_config = ConfigDict( # Configuración del modelo
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
        "_id": "ObjectID(661fd1ddebd2b08c5500722c)",
        "title": "Tacos Dorados de Papa",
        "url": "https://www.mexicoenmicocina.com/tacos-dorados-de-papa/",
        "descripcion": "",
        "source": "Recetas de la abuela",
        "language_ISO": "ES",
        "origin_ISO": "MEX",
        "n_diners": 6,
        "dificultad": "",
        "category": [
            "vegetarianos"
        ],
        "subcategory": "",
        "minutes": 60,
        "n_ingredients": 16,
        "ingredients": [
            "½ taza de cilantro finamente picado",
            "1 taza de tomate picadito y sin semillas",
            "1 cucharada de jugo de limón",
            "12 to rtillas de maíz",
            "⅔ de taza de aceite vegetal para freír los taquitos",
            "2 chiles serranos en cubitos",
            "Sal al gusto",
            "2 tazas de repollo en tiras finas",
            "½ taza de crema mexicana",
            "Salsa roja",
            "½ taza de cebolla blanca en cubitos",
            "3 papas rojas de tamaño mediano ~510 gr. *",
            "24 palillos de madera para sostener los taquitos enrollados",
            "1 aguacate opcional",
            "Sal y pimienta al gusto",
            "½ taza de Queso Cotija o Queso Fresco desmenuzado**"
        ],
        "n_steps": 24,
        "steps": [
            "Pon las papas enteras en una olla mediana y cúbrelas con agua fría",
            "NO peles ni cortes las papas",
            "No queremos que las papas absorban demasiada agua, porque luego esa agua se liberará formando burbujas al freírlas y el aceite salpicará",
            "Pon el fuego a medio alto y cocínalas hasta que estén tiernas (unos 20 a 25 minutos)",
            "Escurre las papas para quitar el excedente de agua y pásalas a un tazón",
            "Espera hasta que estén lo suficientemente frías para que puedas tocarlas y quita las cáscaras",
            "Sazona las papas con sal y pimienta, y machaca hasta que obtengas una consistencia cremosa",
            "No se verá exactamente como puré, sino más como una pastita",
            "Deja a un lado",
            "Calienta aproximadamente ½ taza de aceite en una sartén grande a fuego medio-alto",
            "Agrega el resto del aceite según sea necesario",
            "Mientras esperas a que caliente el aceite, calienta ligeramente las tortillas una por una en un comal, para hacerlas más suaves y se puedan doblar fácilmente",
            "Cúbrelas con una servilleta de cocina",
            "Ahora, agrega 2 cucharadas de puré de papa sobre la mitad de cada tortilla y dóblala",
            "Asegura los lados de la tortilla con dos palillos",
            "A veces, no utilizo palillos, pero eso requiere cierta habilidad para poder presionar firmemente los bordes hacia abajo mientras se fríe; si es la primera vez que los preparas, y para irse a lo seguro, utiliza los palillos",
            "Coloca el taco doblado en el aceite hirviendo, y cocina por un minuto y medio por cada lado, hasta que esté dorado y crujiente",
            "Ya que trabajarás en tandas, ten un plato grande preparado y cubierto con toallas de papel para absorber el exceso de aceite",
            "Repite el proceso hasta que termines de cocinar todos los taquitos",
            ", PARA PREPARAR LA SALSA:Mezcla los ingredientes de la salsa en un tazón mediano y sazona con sal",
            "Deja a un lado",
            "Puedes tener todos los ingredientes listos un día antes, y sólo combinarlos antes de servir",
            "Para servir, quita los palillos (con mucho cuidado para evitar romper las tortillas) y decora con col/repollo rallado, queso cotija y Pico de Gallo",
            "También pueden coronarlos con aguacate y crema"
        ],
        "images": [],
        "interactions": "",
        "aver_rate": "",
        "num_interactions": 0,
        "tags": [],
        "num_tags": "",
        "dietary_preferences": [
            "Alto en calorías",
            "Alto en grasas",
            "Alto en sodio"
        ]
        }
    )
    
    
class AbuelaCollection(BaseModel):
    """
        A container holding a list of `AbuelaModel` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    abuela: List[AbuelaModel]
    
@app.get(
    "/abuela/",
    response_description="Listar todas las recetas de la abuela",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def list_abuela():
    """
    Listar las recetas de la abuela.
    
    La respuesta está limitada a 100 resultados.
    """
    return AbuelaCollection(abuela=await abuela_collection.find().to_list(100))

@app.get(
    "/abuela/{titulo}",
    response_description="Buscar una receta de la abuela",
    response_model=AbuelaCollection,
    response_model_by_alias=False,
)
async def search_abuela(titulo: str):
    """
    Buscar una receta de la abuela por su título.    
    """
    
    recetas = []
    recetas = []
    async for recipe in abuela_collection.find():
        if titulo.lower() in recipe['title'].lower():
            recetas.append(recipe)

    print("Recetas encontradas: ", len(recetas))
    if len(recetas) > 0:
        return AbuelaCollection(abuela=recetas)

    raise HTTPException(status_code=404, detail=f"No se encontraron recetas con el nombre {titulo}")