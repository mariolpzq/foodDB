import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
import pymongo
from pymongo import MongoClient
import json
import os
from concurrent.futures import ThreadPoolExecutor

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection_ingredientes = db['all_ingredients']
collection_recetas = db['food.com']

# Carga del modelo de lenguaje
model = SentenceTransformer('all-mpnet-base-v2')

# Funciones para extraer ingrediente principal y detalles por separado
def get_main_ingredient(name):
    return name.split(',')[0]

def get_details(name):
    parts = name.split(',')
    return ','.join(parts[1:]).strip()

# Carga de info nutricional de la base de datos
cursor = collection_ingredientes.find({})  # Obtener todos los ingredientes

# Crear un DataFrame con los datos de la base de datos
df = pd.DataFrame(list(cursor))

# Extraer ingrediente principal y detalles
df['main_ingredient'] = df['name_en'].apply(get_main_ingredient)
df['ingredient_details'] = df['name_en'].apply(get_details)

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

# Obtenemos los embeddings de los ingredientes de la base de datos
cursor_recetas = collection_recetas.find({})  # Obtener todas las recetas

# Diccionario para almacenar pares ingrediente - ingredienteID
ingredient_cache = {}

# Función para procesar una receta
def process_recipe(receta):
    ingredientes = receta['ingredients']

    # Verificar si alguno de los ingredientes ya tiene ingredientID
    if any('ingredientID' in ingrediente for ingrediente in ingredientes):
        return  # Si ya tiene ingredientID, no procesar esta receta

    updates = []

    for ingrediente_receta in ingredientes:  # Recorrer todos los ingredientes de la receta
        mi_ingrediente = ingrediente_receta['ingredient']
        
        # Verificar si el ingrediente ya está en el diccionario cache
        if mi_ingrediente in ingredient_cache:
            cached_data = ingredient_cache[mi_ingrediente]
            updates.append(
                pymongo.UpdateOne(
                    {'_id': receta['_id'], 'ingredients.ingredient': mi_ingrediente},
                    {'$set': {
                        'ingredients.$.ingredientID': cached_data['ingredientID'],
                        'ingredients.$.max_similarity': cached_data['max_similarity']
                    }}
                )
            )
            continue
        
        # Codificar el ingrediente de la receta
        mi_ingrediente_main = model.encode([get_main_ingredient(mi_ingrediente)])
        mi_ingrediente_details = model.encode([get_details(mi_ingrediente)])

        # Comparar emb con todos los vectores de embeddings
        similarities = cosine_similarity(mi_ingrediente_main.reshape(1, -1), main_ingredient_encoding)

        # Obtener el valor máximo de similitud y las posiciones correspondientes
        max_similarity = np.max(similarities)
        max_similarity_positions = [idx for idx, sim in enumerate(similarities[0]) if sim == max_similarity]

        # Comparar detalles del ingrediente solo para las posiciones con máxima similitud
        similarities_details = cosine_similarity(mi_ingrediente_details.reshape(1, -1), ingredient_details_encoding[max_similarity_positions])
        sorted_indices_details = similarities_details.argsort()[0][::-1]

        max_similarity_positions_sorted = [max_similarity_positions[idx] for idx in sorted_indices_details]

        best_match = dict_df[max_similarity_positions_sorted[0]]

        # Actualizar el diccionario cache
        ingredient_cache[mi_ingrediente] = {
            'ingredientID': best_match['_id'],
            'max_similarity': max_similarity
        }

        updates.append(
            pymongo.UpdateOne(
                {'_id': receta['_id'], 'ingredients.ingredient': mi_ingrediente},
                {'$set': {
                    'ingredients.$.ingredientID': best_match['_id'],
                    'ingredients.$.max_similarity': max_similarity
                }}
            )
        )
    
    if updates:
        collection_recetas.bulk_write(updates)
        print(f"Receta {receta['_id']} actualizada.")

# Procesar recetas en paralelo
with ThreadPoolExecutor() as executor:
    executor.map(process_recipe, cursor_recetas)

print("Proceso completado.")
