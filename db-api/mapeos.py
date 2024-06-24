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

from models import MappingIngredientsRequest, MappingCompoundsRequest, MappingEmissionsRequest
from bd import cofid_collection, recipe1m_collection, mealrec_collection, compounds_collection, emissions_collection, get_collection

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import pymongo
from pymongo import MongoClient
import json

import motor.motor_asyncio



router = APIRouter()

# Carga del modelo de lenguaje
model = SentenceTransformer('all-mpnet-base-v2')
model_esp = SentenceTransformer('hiiamsid/sentence_similarity_spanish_es')

# Funciones para extraer ingrediente principal y detalles por separado
def get_main_ingredient(name):
    return name.split(',')[0]

def get_details(name):
    parts = name.split(',')
    return ','.join(parts[1:]).strip()


# ---------------------------------------------------- MAPEO INGREDIENTES EN INGLÉS ---------------------------------------------------- #

async def map_ingredientes(request: MappingIngredientsRequest):
    print(request)
    try:
        collection_ingredientes = get_collection(request.ingredients_collection)
        print(collection_ingredientes)
        collection_recetas = get_collection(request.recipes_collection)
        print(collection_recetas)

        # Usar los valores proporcionados en el objeto MappingIngredientsRequest
        ingredient_field_name = str(request.ingredient_field_name)
        print(ingredient_field_name)
        recipe_ingredients_array_name = str(request.recipe_ingredients_array_name)
        print(recipe_ingredients_array_name)
        recipe_ingredient_field_name = str(request.recipe_ingredient_field_name)
        print(recipe_ingredient_field_name)

        # Carga de info nutricional de la base de datos
        cursor = collection_ingredientes.find({}) # Obtener todos los ingredientes

        # Crear un DataFrame con los datos de la base de datos
        df = pd.DataFrame(await cursor.to_list(length=None))

        # Extraer ingrediente principal y detalles
        df['main_ingredient'] = df[ingredient_field_name].apply(get_main_ingredient)
        df['ingredient_details'] = df[ingredient_field_name].apply(get_details)

        # Convertimos el DataFrame a un diccionario
        dict_df = df.to_dict('records')

        # Verificar si ya existen archivos JSON con las codificaciones
        if os.path.exists('main_ingredient_encoding.json') and os.path.exists('ingredient_details_encoding.json'):
            # Cargar las codificaciones de los ingredientes desde los archivos JSON
            with open('main_ingredient_encoding.json', 'r') as f:
                main_ingredient_encoding_list = json.load(f)
                main_ingredient_encoding = np.array(main_ingredient_encoding_list)

            with open('ingredient_details_encoding.json', 'r') as f:
                ingredient_details_encoding_list = json.load(f)
                ingredient_details_encoding = np.array(ingredient_details_encoding_list)
        else:
            print("Codificando ingredientes...")
            main_ingredient_encoding = model.encode(list(df['main_ingredient']))
            ingredient_details_encoding = model.encode(list(df['ingredient_details']))

            # Convertir los arrays de NumPy a listas
            main_ingredient_encoding_list = main_ingredient_encoding.tolist()
            ingredient_details_encoding_list = ingredient_details_encoding.tolist()

            # Guardar las codificaciones en archivos JSON
            with open('main_ingredient_encoding.json', 'w') as f:
                json.dump(main_ingredient_encoding_list, f)
            with open('ingredient_details_encoding.json', 'w') as f:
                json.dump(ingredient_details_encoding_list, f)

        # Identificar recetas sin 'ingredientID' en todos los ingredientes
        print("Identificando recetas sin 'ingredientID' en todos los ingredientes...")
        recetas_sin_ingredientID = []

        cursor_recetas = collection_recetas.find({})
        async for receta in cursor_recetas:
            ingredientes = receta[recipe_ingredients_array_name]
            todos_sin_ingredientID = all('ingredientID' not in ingrediente for ingrediente in ingredientes)
            if todos_sin_ingredientID:
                recetas_sin_ingredientID.append(receta)

        # Procesar solo las recetas sin 'ingredientID' en todos los ingredientes
        print("Procesando recetas sin 'ingredientID' en todos los ingredientes...")
        for receta in recetas_sin_ingredientID:
            ingredientes = receta[recipe_ingredients_array_name]
            for ingrediente_receta in ingredientes:
                # Codificar el ingrediente de la receta
                mi_ingrediente = ingrediente_receta[recipe_ingredient_field_name]
                mi_ingrediente_main = model.encode([get_main_ingredient(mi_ingrediente)])
                mi_ingrediente_details = model.encode([get_details(mi_ingrediente)])

                print(ingrediente_receta[recipe_ingredient_field_name])

                # Comparar emb con todos los vectores de embeddings
                similarities = np.array(cosine_similarity(mi_ingrediente_main.reshape(1, -1), main_ingredient_encoding))

                # Obtener los índices de los embeddings ordenados por similitud descendente
                sorted_indices = similarities.argsort()[0][::-1]

                # Obtener el valor máximo de similitud alcanzado
                max_similarity = np.max(similarities)
                max_similarity_positions = [idx for idx, sim in enumerate(similarities[0]) if sim == max_similarity]

                # Imprimir el valor máximo de similitud y los alimentos principales correspondientes
                print("Máxima similitud alcanzada:", max_similarity)
                print("\nAlimentos principales con máxima similitud:")
                for pos in max_similarity_positions:
                    print(dict_df[pos][ingredient_field_name])

                # Identificación de la parte detallada del ingrediente
                similarities = np.array(cosine_similarity(mi_ingrediente_details.reshape(1, -1), ingredient_details_encoding[max_similarity_positions]))
                sorted_indices = similarities.argsort()[0][::-1]
                max_similarity_positions_sorted = [max_similarity_positions[idx] for idx in sorted_indices]

                print(max_similarity_positions_sorted)
                for pos in max_similarity_positions_sorted:
                    print(dict_df[pos][ingredient_field_name])

                # Actualizar el ingrediente en la receta
                collection_recetas.update_one(
                    {'_id': receta['_id'], f'{recipe_ingredients_array_name}.{recipe_ingredient_field_name}': mi_ingrediente},
                    {'$set': {
                        f'{recipe_ingredients_array_name}.$.ingredientID': dict_df[max_similarity_positions_sorted[0]]['_id'],
                        f'{recipe_ingredients_array_name}.$.max_similarity': float(max_similarity)
                    }}
                )

    except Exception as e:
        raise HTTPException(status_code=501, detail=str(e))



# Ruta para el mapeo de ingredientes
@router.post("/map-ingredients/")
async def map_ingredientes_route(request: MappingIngredientsRequest):
    try:
        await map_ingredientes(request)
        return {"message": "Mapeo de ingredientes completado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# ---------------------------------------------------- MAPEO INGREDIENTES EN ESPAÑOL ---------------------------------------------------- #

async def map_ingredientes_esp(request: MappingIngredientsRequest):

    try:
        collection_ingredientes = get_collection(request.ingredients_collection)
        print(collection_ingredientes)
        collection_recetas = get_collection(request.recipes_collection)
        print(collection_recetas)

        # Usar los valores proporcionados en el objeto MappingIngredientsRequest
        ingredient_field_name = str(request.ingredient_field_name)
        print(ingredient_field_name)
        recipe_ingredients_array_name = str(request.recipe_ingredients_array_name)
        print(recipe_ingredients_array_name)
        recipe_ingredient_field_name = str(request.recipe_ingredient_field_name)
        print(recipe_ingredient_field_name)

        # Carga de info nutricional de la base de datos

        cursor = collection_ingredientes.find({}) # Obtener todos los ingredientes

        # Crear un DataFrame con los datos de la base de datos

        df = pd.DataFrame(await cursor.to_list(length=None)) 

        # Extraer ingrediente principal y detalles

        df['main_ingredient'] = df[ingredient_field_name].apply(get_main_ingredient)
        df['ingredient_details'] = df[ingredient_field_name].apply(get_details)

        # Convertimos el DataFrame a un diccionario

        dict_df = df.to_dict('records')


        # Verificar si ya existen archivos JSON con las codificaciones
        if os.path.exists('main_ingredient_esp_encoding.json') and os.path.exists('ingredient_details_esp_encoding.json'):
            # Cargar las codificaciones de los ingredientes desde los archivos JSON
            with open('main_ingredient_esp_encoding.json', 'r') as f:
                main_ingredient_encoding_list = json.load(f)
                main_ingredient_encoding = np.array(main_ingredient_encoding_list)

            with open('ingredient_details_esp_encoding.json', 'r') as f:
                ingredient_details_encoding_list = json.load(f)
                ingredient_details_encoding = np.array(ingredient_details_encoding_list)
        else:
            print("Codificando ingredientes...")
            main_ingredient_encoding = model_esp.encode(list(df['main_ingredient']))
            ingredient_details_encoding = model_esp.encode(list(df['ingredient_details']))

            # Convertir los arrays de NumPy a listas
            main_ingredient_encoding_list = main_ingredient_encoding.tolist()
            ingredient_details_encoding_list = ingredient_details_encoding.tolist()

            # Guardar las codificaciones en archivos JSON
            with open('main_ingredient_esp_encoding.json', 'w') as f:
                json.dump(main_ingredient_encoding_list, f)
            with open('ingredient_details_esp_encoding.json', 'w') as f:
                json.dump(ingredient_details_encoding_list, f)


        # Identificar recetas sin 'ingredientID' en todos los ingredientes
        print("Identificando recetas sin 'ingredientID' en todos los ingredientes...")
        recetas_sin_ingredientID = []

        cursor_recetas = collection_recetas.find({})
        async for receta in cursor_recetas:
            ingredientes = receta[recipe_ingredients_array_name]
            todos_sin_ingredientID = all('ingredientID' not in ingrediente for ingrediente in ingredientes)
            if todos_sin_ingredientID:
                recetas_sin_ingredientID.append(receta)

        # Procesar solo las recetas sin 'ingredientID' en todos los ingredientes
        print("Procesando recetas sin 'ingredientID' en todos los ingredientes...")
        for receta in recetas_sin_ingredientID:

            ingredientes = receta[recipe_ingredients_array_name]

            for ingrediente_receta in ingredientes: # Recorrer todos los ingredientes de la receta

                # Codificar el ingrediente de la receta

                mi_ingrediente = ingrediente_receta[recipe_ingredient_field_name]
                mi_ingrediente_main = model_esp.encode([get_main_ingredient(mi_ingrediente)])
                mi_ingrediente_details = model_esp.encode([get_details(mi_ingrediente)])

                print(ingrediente_receta[recipe_ingredient_field_name])

                # Comparar emb con todos los vectores de embeddings
                similarities = np.array(cosine_similarity(mi_ingrediente_main.reshape(1, -1), main_ingredient_encoding))

                # Obtener los índices de los embeddings ordenados por similitud descendente
                sorted_indices = similarities.argsort()[0][::-1]

                # nos quedamos con el valor máximo de similitud alcanzado, y queremos obtener todos los alimentos principales que den ese valor máximo. Puede dar más de uno.
                max_similarity = np.max(similarities)
                # Obtener todos los alimentos principales que dan ese valor máximo
                max_similarity_positions = [idx for idx, sim in enumerate(similarities[0]) if sim == max_similarity]

                # Imprimir el valor máximo de similitud y los alimentos principales correspondientes
                print("Máxima similitud alcanzada:", max_similarity)
                print("\nAlimentos principales con máxima similitud (solo nos fijamos en lo que hay antes de la primera coma):")
                for pos in max_similarity_positions:
                    print(dict_df[pos][ingredient_field_name])

                """## 2.2 Identificación de la parte detallada del ingrediente (todo lo que sigue la primera coma)
                Una vez tenemos la coincidencia máxima de ingrediente (en general), miramos la info detallada para intentar acertar al máximo. Usamos la misma metodología, pero esta vez únicamente nos quedamos con el que nos de la descripción más acertada de todas.
                """

                print("Bien")
                
                similarities = np.array(cosine_similarity(mi_ingrediente_details.reshape(1, -1), ingredient_details_encoding[max_similarity_positions]))
                sorted_indices = similarities.argsort()[0][::-1]

                # Obtener los alimentos principales que corresponden a los índices ordenados
                max_similarity_positions_sorted = [max_similarity_positions[idx] for idx in sorted_indices]

                print(max_similarity_positions_sorted)

                for pos in max_similarity_positions_sorted:
                    print(dict_df[pos][ingredient_field_name])

                """### Resultado

                Y la opción final más parecida, sería la que aparece en este último vector ordenado en la posición 0

                """

                print(dict_df[max_similarity_positions_sorted[0]])


                collection_recetas.update_one(
                {   # Modificar la condición de búsqueda
                    '_id': receta['_id'], 
                    f'{recipe_ingredients_array_name}.{recipe_ingredient_field_name}': mi_ingrediente
                },
                {'$set': {
                    f'{recipe_ingredients_array_name}.$.ingredientID': dict_df[max_similarity_positions_sorted[0]]['_id'], 
                    f'{recipe_ingredients_array_name}.$.max_similarity': float(max_similarity)
                }}
            )
                
    except Exception as e:
        raise HTTPException(status_code=501, detail=str(e))

# Ruta para el mapeo de ingredientes
@router.post("/map-ingredients-esp/")
async def map_ingredientes_esp_route(request: MappingIngredientsRequest):
    try:
        await map_ingredientes_esp(request)
        return {"message": "Mapeo de ingredientes completado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# ---------------------------------------------------- MAPEO SABORES ---------------------------------------------------- #

"""
ingredients_collection: str = Field(..., description="Nombre de la colección de ingredientes")
    ingredient_field_name: str = Field(..., description="Nombre del campo que contiene el nombre del ingrediente")
    compounds_collection: str = Field(..., description="Nombre de la colección de compuestos")
    compound_field_name: str = Field(..., description="Nombre del campo que contiene los compuestos del ingrediente")
    
"""

async def map_sabores(request: MappingCompoundsRequest):

    try:
       
        collection_ingredientes = get_collection(request.ingredients_collection)
        print(collection_ingredientes)
        collection_sabores = get_collection(request.compounds_collection)
        print(collection_sabores)

        ingredient_field_name = str(request.ingredient_field_name)
        compound_ingredient_field_name = str(request.compound_ingredient_field_name)


        # Carga de sabores de la base de datos

        cursor = collection_sabores.find({}) # Obtener todos los sabores

        # Crear un DataFrame con los datos de la base de datos

        df = pd.DataFrame(await cursor.to_list(length=None)) 

        dict_df = df.to_dict('records')

        print("Codificando sabores...")

        compounds_ingredient_encoding = model.encode(list(df[compound_ingredient_field_name]))

        # Obtenemos los embeddings de los ingredientes de la base de datos

        cursor_ingredientes = collection_ingredientes.find({}) # Obtener todos los ingredientes

        print("Recorremos todos los ingredientes...")

        async for ingrediente in cursor_ingredientes: # Recorrer todas los ingredientes

            mi_ingrediente = ingrediente[ingredient_field_name]
            mi_ingrediente_main = model.encode([get_main_ingredient(mi_ingrediente)])

            print(ingrediente[ingredient_field_name])

            # Comparar emb con todos los vectores de embeddings
            similarities = np.array(cosine_similarity(mi_ingrediente_main.reshape(1, -1), compounds_ingredient_encoding))
            print("Similarities: " + str(len(similarities)))


            # Obtener los índices de los embeddings ordenados por similitud descendente
            sorted_indices = similarities.argsort()[0][::-1]

            print("Sorted indices: " + str(len(sorted_indices)))

            # nos quedamos con el valor máximo de similitud alcanzado, y queremos obtener todos los alimentos principales que den ese valor máximo. Puede dar más de uno.
            max_similarity = np.max(similarities)
            print("Max similarity: " + str(max_similarity))
            # Obtener todos los alimentos principales que dan ese valor máximo
            max_similarity_positions = [idx for idx, sim in enumerate(similarities[0]) if sim == max_similarity]
            print("Max similarity positions: " + str(len(max_similarity_positions)))
            # Obtener los alimentos principales que corresponden a los índices ordenados
            if len(max_similarity_positions) > 1:
                max_similarity_positions_sorted = [max_similarity_positions[idx] for idx in sorted_indices]
                print("Max similarity positions sorted: " + str(len(max_similarity_positions_sorted)))
            else:
                max_similarity_positions_sorted = max_similarity_positions

            # Imprimir el valor máximo de similitud y los sabores principales correspondientes
            print("Máxima similitud alcanzada:", max_similarity)
            print("\Sabores con máxima similitud (solo nos fijamos en lo que hay antes de la primera coma):")
            for pos in max_similarity_positions:
                print(dict_df[pos][compound_ingredient_field_name])

            for pos in max_similarity_positions_sorted:
                print(dict_df[pos][compound_ingredient_field_name])

            if similarities[0][max_similarity_positions_sorted[0]] > 0.7:
                compound_data = dict_df[max_similarity_positions_sorted[0]]
                compound_data['max_similarity'] = float(max_similarity)
                collection_ingredientes.update_one({'_id': ingrediente['_id']}, {'$set': {'compounds': [compound_data]}})
                print("Ingrediente actualizado:", ingrediente[ingredient_field_name])

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
# Ruta para el mapeo de sabores
@router.post("/map-compounds/")
async def map_sabores_route(request: MappingCompoundsRequest):
    try:
        await map_sabores(request)
        return {"message": "Mapeo de sabores completado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    


# ---------------------------------------------------- EMISIONES ---------------------------------------------------- #

async def map_emisiones(request: MappingEmissionsRequest):

    try:

        collection_ingredientes = get_collection(request.ingredients_collection)
        print(collection_ingredientes)
        collection_emisiones = get_collection(request.emissions_collection)
        print(collection_emisiones)

        ingredient_field_name = str(request.ingredient_field_name)
        emission_ingredient_field_name = str(request.emission_ingredient_field_name)

        cursor = collection_emisiones.find({}) # Obtener todas las emisiones

        # Crear un DataFrame con los datos de la base de datos

        df = pd.DataFrame(await cursor.to_list(length=None)) 

        # Convertimos el DataFrame a un diccionario

        dict_df = df.to_dict('records')

        # Verificar si ya existen archivos JSON con las codificaciones

        print("Codificando emisiones...")

        emissions_ingredient_encoding = model.encode(list(df[emission_ingredient_field_name]))


        # Obtenemos los embeddings de los ingredientes de la base de datos

        cursor_ingredientes = collection_ingredientes.find({}) # Obtener todas los ingredientes

        print("Recorremos todos los ingredientes...")

        async for ingrediente in cursor_ingredientes:

            mi_ingrediente = ingrediente[ingredient_field_name]
            mi_ingrediente_main = model.encode([get_main_ingredient(mi_ingrediente)])

            print(ingrediente[ingredient_field_name])

            # Comparar emb con todos los vectores de embeddings
            similarities = np.array(cosine_similarity(mi_ingrediente_main.reshape(1, -1), emissions_ingredient_encoding))
            print("Similarities: " + str(len(similarities)))


            # Obtener los índices de los embeddings ordenados por similitud descendente
            sorted_indices = similarities.argsort()[0][::-1]

            print("Sorted indices: " + str(len(sorted_indices)))

            # nos quedamos con el valor máximo de similitud alcanzado, y queremos obtener todos los alimentos principales que den ese valor máximo. Puede dar más de uno.
            max_similarity = np.max(similarities)
            print("Max similarity: " + str(max_similarity))
            # Obtener todos los alimentos principales que dan ese valor máximo
            max_similarity_positions = [idx for idx, sim in enumerate(similarities[0]) if sim == max_similarity]
            print("Max similarity positions: " + str(len(max_similarity_positions)))
            # Obtener los alimentos principales que corresponden a los índices ordenados
            if len(max_similarity_positions) > 1:
                max_similarity_positions_sorted = [max_similarity_positions[idx] for idx in sorted_indices]
                print("Max similarity positions sorted: " + str(len(max_similarity_positions_sorted)))
            else:
                max_similarity_positions_sorted = max_similarity_positions

            # Imprimir el valor máximo de similitud y los alimentos principales correspondientes
            print("Máxima similitud alcanzada:", max_similarity)
            print("\Emisiones con máxima similitud (solo nos fijamos en lo que hay antes de la primera coma):")
            for pos in max_similarity_positions:
                print(dict_df[pos][emission_ingredient_field_name])

            for pos in max_similarity_positions_sorted:
                print(dict_df[pos][emission_ingredient_field_name])

            if similarities[0][max_similarity_positions_sorted[0]] > 0.7: # Accedemos al valor de similitud almacenado en la matriz de similitudes para el primer ingrediente más similar.
                collection_ingredientes.update_one({'_id': ingrediente['_id']}, {'$set': {'emissionsID': dict_df[max_similarity_positions_sorted[0]]['_id']}})
                print("Ingrediente actualizado: " + ingrediente[ingredient_field_name])
            
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    

# Ruta para el mapeo de emisiones
@router.post("/map-emissions/")
async def map_emisiones_route(request: MappingEmissionsRequest):
    try:
        await map_emisiones(request)
        return {"message": "Mapeo de emisiones completado"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
            

 



