import os
from typing import Optional, List, Union
from datetime import datetime

from fastapi import FastAPI, Body, HTTPException, status, APIRouter
from fastapi.responses import Response
from pydantic import ConfigDict, BaseModel, Field, EmailStr
from pydantic.functional_validators import BeforeValidator

from typing_extensions import Annotated

from bson import ObjectId
import motor.motor_asyncio
from pymongo import ReturnDocument
from bson import ObjectId


from pydantic import BaseModel, Field
from typing import List, Union, Dict


# Represents an ObjectId field in the database.
# It will be represented as a `str` on the model so that it can be serialized to JSON.
PyObjectId = Annotated[str, BeforeValidator(str)]


# ---------------------------------------------------- COMPUESTOS ---------------------------------------------------- #

class CompoundModel(BaseModel): 
    """
    Container para un compuesto.
    """   
    
    
    ingredient : str = Field(...)
    compounds : List[str] = Field(...)
    
    model_config = ConfigDict( 
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "ingredient": "almond",
            "compounds": [
                "60-18-4",
                "1072-83-9",
                "71-00-1",
                "14901-07-6",
                "765-70-8",
                "611-13-2",
                "23747-48-0",
                "14667-55-1",
                "108-95-2"
            ]
        }
    )


class CompoundCollection(BaseModel):
    """
        A container holding a list of `CompoundModel` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    compounds: List[CompoundModel]

# ---------------------------------------------------- INGREDIENTES ---------------------------------------------------- #

class IngredientModel(BaseModel): # Modelo de ingrediente
    """
    Container para un ingrediente.
    """   

    id: Optional[PyObjectId] = Field(alias="_id", default=None) # El alias es para que en la base de datos se guarde como _id
    name_esp : str = Field(...)
    name_en : str = Field(...)
    langual :  str = Field("")
    origin_ISO : str = Field(...)
    source : str = Field(...)
    category_esp : str = Field(...)
    category_en : str = Field(...)
    edible :  Union[float,str] = Field(...)
    compounds : List[CompoundModel] = Field(...)
    nutritional_info_100g : dict = Field(...)
    oms_lights : dict = Field(...)
    emissionsID: Optional[PyObjectId] = Field(None, alias="emissionsID")
    
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
            "emissionsID": "ObjectID(66261bfd6f790019dbc6b221)"
        }
    )
    
    
class IngredientCollection(BaseModel):
    """
        A container holding a list of `Ingrediente` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    ingredientes: List[IngredientModel]
    
    
class IngredientRecipeModel(BaseModel):
    ingredient: str
    ingredientID: Optional[PyObjectId] = None
    max_similarity: Optional[float] = None

    class Config:
        json_encoders = {ObjectId: str}

class IngredientRecipeCollection(BaseModel):
    """
        A container holding a list of `IngredientRecipeModel` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    ingredientes: List[IngredientRecipeModel]

    
# ---------------------------------------------------- RECETAS ---------------------------------------------------- #

class RecipeModel(BaseModel): 
    """
    Container para una receta.
    """

    id: Optional[PyObjectId]= Field(alias="_id", default=None)
    title : Optional[str] = Field(...)
    url: Optional[Union[dict,str]] = Field(None)
    URL: Optional[Union[dict,str]] = Field(None)
    source : Optional[str] = Field(...)
    language_ISO : Optional[str] = Field(...)
    origin_ISO : Optional[str] = Field(...)
    n_diners : Optional[Union[str,int]] = Field(...)
    dificultad : Optional[str] = Field("")
    category : Optional[Union[List[str],str]] = Field(...)
    subcategory : Optional[str] = Field(...)
    minutes : Optional[Union[str,int]] = Field(...)
    n_ingredients : Optional[Union[str,int]] = Field(None)
    ingredients: Optional[ Union[ List[Union[PyObjectId, str, List[str], List[dict], List[IngredientModel]]], str]] = Field(None)
    n_steps : Optional[int] = Field(...)
    steps : Optional[Union[List[str], List[dict]]]= Field(...)
    images : Optional[List[str]] = Field(...)
    interactions: Optional[Union[List[dict],dict,str]] = Field(None)
    aver_rate : Optional[Union[dict,float,str]] = Field(None)
    num_interactions : Optional[int] = Field(None)
    tags : Optional[List[str]] = Field(None)
    num_tags : Optional[Union[int,str]] = Field(None)
    nutritional_info_100g : Optional[dict] = Field({})
    nutritional_info_PDV : Optional[dict] = Field({})
    FSA_lights_per100g : Optional[dict] = Field({})
    OMS_lights_per100g : Optional[dict] = Field({})
    dietary_preferences : Optional[List[str]] = Field(None)

    model_config = ConfigDict( # Configuración del modelo
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "_id": "ObjectID(661fd1ddebd2b08c5500722c)",
            "title": "Tacos Dorados de Papa",
            "URL": "https://www.mexicoenmicocina.com/tacos-dorados-de-papa/",
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
            "ingredients": {
                        "original_ingredient": "8 ounces, weight Light Fat Free Vanilla Yogurt (I Used Activia)",
                        "ingredient": "yogurt, greek, plain, nonfat",
                        "quantity": "8",
                        "unit": "ounce",
                        "weight": 226.796,
                        "nutr_per_ingredient": {
                            "fat": 0.8845044000000001,
                            "nrg": 133.80964,
                            "pro": 23.110512399999998,
                            "sat": 0.26535132,
                            "sod": 81.64656,
                            "sug": 7.348190400000001
                        },
                        "ingredientID": "66261c519801b15acce7afb0"
            },
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
                "Ya que trabajarás en tandas, ten un plato grande preparado y cubi"
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
            "nutritional_info_100g": {
                "energy": "",
                "car": "",
                "pro": "",
                "fat": "",
                "sat": "",
            },
            "nutritional_info_PDV": {
                "energy": "",
                "fat": "",
                "car": "",
                "pro": "",
                "sat": "",
                "salt": "",
                "sug": "",
            },
            "FSA_lights_per100g": {
                "fat": "",
                "salt": "",
                "sat": "",
                "sug": "",
                "energy": "",
                "sod": "",
                "fiber": "",
                "pro": "",
            },
            "OMS_lights_per100g": {
                "fat": "",
                "trans": "",
                "salt": "",
                "sug": "",
            },
            "dietary_preferences": [
                "Alto en calorías",
                "Alto en grasas",
                "Alto en sodio"
            ]
        }
    )


class RecipeCollection(BaseModel):
    """
        A container holding a list of `RecipeModel` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    recetas: List[RecipeModel]

class ShortRecipeModel(BaseModel): 
    """
    Container para una receta.
    """

    id: Optional[PyObjectId]= Field(alias="_id", default=None)
    title : Optional[str] = Field(...) 
    category : Optional[Union[List[str],str]] = Field(...)

    model_config = ConfigDict( # Configuración del modelo
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "_id": "ObjectID(661fd1ddebd2b08c5500722c)",
            "title": "Tacos Dorados de Papa",
            "category": "appetizer"
        }
    )

class ShortRecipeCollection(BaseModel):

    recetas: List[ShortRecipeModel]


# ---------------------------------------------------- RECETAS DE MEALREC ---------------------------------------------------- #

class MealRECRecipeModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)
    title: Optional[str] = Field(...)
    url: Optional[Union[dict, str]] = Field(None)
    source: Optional[str] = Field(...)
    language_ISO: Optional[str] = Field(...)
    origin_ISO: Optional[str] = Field(...)
    n_diners: Optional[Union[str, int]] = Field(...)
    dificultad: Optional[str] = Field("")
    category: Optional[Union[List[str], str]] = Field(...)
    subcategory: Optional[str] = Field(...)
    minutes: Optional[Union[str, int]] = Field(...)
    n_ingredients: Optional[Union[str, int]] = Field(None)
    ingredients: Optional[List[IngredientRecipeModel]] = Field(None)
    n_steps: Optional[int] = Field(...)
    steps: Optional[Union[List[str], List[dict]]] = Field(...)
    images: Optional[List[str]] = Field(...)
    interactions: Optional[Union[List[dict], dict, str]] = Field(None)
    aver_rate: Optional[Union[dict, float, str]] = Field(None)
    num_interactions: Optional[int] = Field(None)
    tags: Optional[List[str]] = Field(None)
    num_tags: Optional[Union[int, str]] = Field(None)
    nutritional_info_100g: Optional[dict] = Field({})
    nutritional_info_PDV: Optional[dict] = Field({})
    FSA_lights_per100g: Optional[dict] = Field({})
    OMS_lights_per100g: Optional[dict] = Field({})
    dietary_preferences: Optional[List[str]] = Field(None)

    model_config = ConfigDict(  # Configuración del modelo
        populate_by_name=True,
        arbitrary_types_allowed=True,
    )

class MealRECRecipeCollection(BaseModel):
    """
        A container holding a list of `MealRECRecipeModel` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    recetas: List[MealRECRecipeModel]
            
# ---------------------------------------------------- RECETAS DE LA ABUELA ---------------------------------------------------- #
    
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
    
    id: Optional[PyObjectId] = Field(alias="_id", default=None) 
    title : str = Field(...)
    url : str = Field(...)
    descripcion : str = Field(...)
    source : str = Field(...)
    language_ISO : str = Field(...)
    origin_ISO : str = Field(...)
    n_diners : Union[str,int] = Field(...)
    dificultad : str = Field(...)
    category : str = Field(...)
    subcategory : List[str] = Field(...)
    minutes : int = Field(...)
    n_ingredients : int = Field(...)
    ingredients: Optional[List[IngredientRecipeModel]] = Field(None)
    n_steps : int = Field(...)
    steps : List[str] = Field(...)
    images : List[str] = Field(...)
    interactions: Optional[Union[List[dict], dict, str]] = Field(None)
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

    recetas: List[AbuelaModel]
    
    
    
# ---------------------------------------------------- MAPEO DE INGREDIENTES ---------------------------------------------------- #

class MappingIngredientsRequest(BaseModel):
    ingredients_collection: str = Field(..., description="Nombre de la colección de ingredientes")
    ingredient_field_name: str = Field(..., description="Nombre del campo que contiene el nombre del ingrediente")
    recipes_collection: str = Field(..., description="Nombre de la colección de recetas")
    recipe_ingredients_array_name: str = Field(..., description="Nombre del array de ingredientes de la receta")
    recipe_ingredient_field_name: str = Field(..., description="Nombre del campo que contiene un ingrediente de la receta dentro del array")

    model_config = ConfigDict( # Configuración del modelo
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "ingredients_collection": "cofid",
            "ingredient_field_name": "name_en",
            "recipes_collection": "recipe1m",
            "recipe_ingredients_array_name": "ingredients",
            "recipe_ingredient_field_name": "ingredient"
        },

    )


class MappingCompoundsRequest(BaseModel):
    ingredients_collection: str = Field(..., description="Nombre de la colección de ingredientes")
    ingredient_field_name: str = Field(..., description="Nombre del campo que contiene el nombre del ingrediente")
    compounds_collection: str = Field(..., description="Nombre de la colección de compuestos")
    compound_ingredient_field_name: str = Field(..., description="Nombre del campo que contiene el nombre del ingrediente")

    model_config = ConfigDict( # Configuración del modelo
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "ingredients_collection": "cofid",
            "ingredient_field_name": "name_en",
            "compounds_collection": "compounds",
            "compound_ingredient_field_name": "ingredient"
        },

    )

class MappingEmissionsRequest(BaseModel):
    ingredients_collection: str = Field(..., description="Nombre de la colección de ingredientes")
    ingredient_field_name: str = Field(..., description="Nombre del campo que contiene el nombre del ingrediente")
    emissions_collection: str = Field(..., description="Nombre de la colección de emisiones")
    emission_ingredient_field_name: str = Field(..., description="Nombre del campo que contiene el nombre del ingrediente")

    model_config = ConfigDict( # Configuración del modelo
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_schema_extra={
            "ingredients_collection": "cofid",
            "ingredient_field_name": "name_en",
            "emissions_collection": "emissions",
            "emission_ingredient_field_name": "name_en"
        },

    )


# ---------------------------------------------------- DIETAS ---------------------------------------------------- #


class DietCompleteModel(BaseModel):
    id: Optional[PyObjectId] = Field(None, alias="_id")
    appetizerID: Optional[PyObjectId] = Field(None, alias="appetizerID")
    main_dishID: Optional[PyObjectId] = Field(None, alias="main_dishID")
    dessertID: Optional[PyObjectId] = Field(None, alias="dessertID")
    appetizer: Optional[MealRECRecipeModel] = Field(None)
    main_dish: Optional[MealRECRecipeModel] = Field(None)
    dessert: Optional[MealRECRecipeModel] = Field(None)
    dietary_preferences: List[str] = Field(...)
    created_at: datetime = Field(None)
    
    class Config:
        allow_population_by_field_name = True
        json_encoders = {ObjectId: str}

class DietCompleteCollection(BaseModel):
    diets: List[DietCompleteModel]

class DietModel(BaseModel):
    appetizerID: Optional[PyObjectId] = Field(None)
    main_dishID: Optional[PyObjectId] = Field(None)
    dessertID: Optional[PyObjectId] = Field(None)

    class Config:
        json_encoders = {ObjectId: str}

class DietCollection(BaseModel):
    diets: List[DietModel]

# ---------------------------------------------------- AUTENTICACIÓN ---------------------------------------------------- #

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    username: Optional[str] = None



class UserModel(BaseModel):
    name: str = Field(...)
    email: EmailStr = Field(...)
    password: str = Field(...)
    gender: str = Field(...)
    age: int = Field(...)
    height: float = Field(...)
    weight: float = Field(...)
    activity_level: int = Field(...)
    daily_caloric_intake: int = Field(...)
    restrictions_kcal: Optional[dict] = Field(default={})
    restrictions_grams: Optional[dict] = Field(default={})
    dietary_preferences: Optional[List[str]] = Field(default=[])
    role: str = Field(default="user")
    diets: Optional[List[DietModel]] = Field(default_factory=list)
    preferences: Optional[dict] = Field(default=None)

    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True,
        json_encoders={ObjectId: str},  # Convertir ObjectId a str para que pueda ser serializado a JSON
        json_schema_extra={
            "name": "Mario López",
            "email": "mario@egmail.com",
            "password": "hashed_password",
            "gender": "male",
            "age": 22,
            "height": 189.0,
            "weight": 75.0,
            "activity_level": "moderate",
            "daily_caloric_intake": 2500,
            "restrictions_kcal": {},
            "restrictions_grams": {},
            "dietary_preferences": ["vegan"],
            "role": "user",  # user, nutritionist, researcher, admin
            "diets": [],
            "preferences": {
                "languages": ["en"],
                "cuisines": ["esp", "mex", "arg"],
            },
        }
    )

    def __str__(self):
        return self.name


class UserCollection(BaseModel):
    """
        A container holding a list of `UserModel` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    users: List[UserModel]


# ---------------------------------------------------- EMISIONES ---------------------------------------------------- #


class EutoModel(BaseModel):
    euto_1000kcal: Optional[Union[float, None]] = Field(None)
    euto_100gr_protein: Optional[Union[float, None]] = Field(None)
    euto_kilogram: Optional[Union[float, None]] = Field(None)

class WithdrawalsModel(BaseModel):
    withdrawals_1000kcal: Optional[Union[float, None]] = Field(None)
    withdrawals_100gr_protein: Optional[Union[float, None]] = Field(None)
    withdrawals_kilogram: Optional[Union[float, None]] = Field(None)

class GreenhouseModel(BaseModel):
    greenhouse_1000kcal: Optional[Union[float, None]] = Field(None)
    greenhouse_100gr_protein: Optional[Union[float, None]] = Field(None)

class LandUseModel(BaseModel):
    land_use_1000kcal: Optional[Union[float, None]] = Field(None)
    land_use_100gr_protein: Optional[Union[float, None]] = Field(None)
    land_use_kilogram: Optional[Union[float, None]] = Field(None)

class ScarcityWaterUseModel(BaseModel):
    scarcity_water_use_1000kcal: Optional[Union[float, None]] = Field(None)
    scarcity_water_use_100gr_protein: Optional[Union[float, None]] = Field(None)
    scarcity_water_use_kilogram: Optional[Union[float, None]] = Field(None)

class EmissionModel(BaseModel):
    id: Optional[PyObjectId] = Field(alias="_id", default=None)  # Usamos alias para el campo _id
    name_esp: str = Field(...)
    name_en: str = Field(...)
    land_use_change: float = Field(...)
    animal_feed: float = Field(...)
    farm: float = Field(...)
    processing: float = Field(...)
    transport: float = Field(...)
    packaging: float = Field(...)
    retail: float = Field(...)
    total_emissions: float = Field(...)

    euto: EutoModel = Field(...)
    withdrawals: WithdrawalsModel = Field(...)
    greenhouse: GreenhouseModel = Field(...)
    land_use: LandUseModel = Field(...)
    scarcity_water_use: ScarcityWaterUseModel = Field(...)

    class Config:
        arbitrary_types_allowed = True
        json_schema_extra = {
            "_id": "ObjectID(6615bacf457fd231f7d62d02)",
            "name_esp": "Trigo y centeno (pan)",
            "name_en": "Wheat & Rye (Bread)",
            "land_use_change": 0.1,
            "animal_feed": 0,
            "farm": 0.8,
            "processing": 0.2,
            "transport": 0.1,
            "packaging": 0.1,
            "retail": 0.1,
            "total_emissions": 1.4,
            "euto": {
                "euto_1000kcal": None,
                "euto_100gr_protein": None,
                "euto_kilogram": None
            },
            "withdrawals": {
                "withdrawals_1000kcal": None,
                "withdrawals_100gr_protein": None,
                "withdrawals_kilogram": None
            },
            "greenhouse": {
                "greenhouse_1000kcal": None,
                "greenhouse_100gr_protein": None
            },
            "land_use": {
                "land_use_1000kcal": None,
                "land_use_100gr_protein": None,
                "land_use_kilogram": None
            },
            "scarcity_water_use": {
                "scarcity_water_use_1000kcal": None,
                "scarcity_water_use_100gr_protein": None,
                "scarcity_water_use_kilogram": None
            }
        }

class EmissionCollection(BaseModel):
    """
        A container holding a list of `EmissionModel` instances.

        This exists because providing a top-level array in a JSON response can be a [vulnerability](https://haacked.com/archive/2009/06/25/json-hijacking.aspx/)
    """

    emissions: List[EmissionModel]
