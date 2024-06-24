#!pip install transformers

#!pip install sentence_transformers

import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer
import numpy as np
#import bd
import pymongo
from pymongo import MongoClient
import json
import os



# Carga de la base de datos 

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection_ingredientes = db['cofid']
collection_sabores = db['compounds']

# Carga del modelo de lenguaje

model = SentenceTransformer('all-mpnet-base-v2')

# Funciones para extraer ingrediente principal y detalles por separado

def get_main_ingredient(name):
    return name.split(',')[0]

def get_details(name):
    parts = name.split(',')
    return ','.join(parts[1:]).strip()

# Carga de sabores de la base de datos

cursor = collection_sabores.find({}) # Obtener todos los sabores

# Crear un DataFrame con los datos de la base de datos

df = pd.DataFrame(list(cursor))

# Convertimos el DataFrame a un diccionario

dict_df = df.to_dict('records')

# Verificar si ya existen archivos JSON con las codificaciones


if os.path.exists('compounds_encoding.json') and os.path.exists('compounds_encoding.json'):
    # Cargar las codificaciones de los sabores desde los archivos JSON
    with open('compounds_encoding.json', 'r') as f:
        compounds_encoding_list = json.load(f)
        compounds_ingredient_encoding = np.array(compounds_encoding_list)

else:
    print("Codificando sabores...")

    compounds_ingredient_encoding = model.encode(list(df['ingredient']))

    # Convertir los arrays de NumPy a listas
    compounds_encoding_list = compounds_ingredient_encoding.tolist()

    # Guardar las codificaciones en archivos JSON
    with open('compounds_encoding.json', 'w') as f:
        json.dump(compounds_encoding_list, f)



# Obtenemos los ingredientes de la base de datos

cursor_ingredientes = collection_ingredientes.find({}) # Obtener todas los ingredientes


# Recorremos todas las ingredientes

print("Recorremos todos los ingredientes...")

for ingrediente in cursor_ingredientes: 

    mi_ingrediente = ingrediente['name_en']
    mi_ingrediente_main = model.encode([get_main_ingredient(mi_ingrediente)])

    print(ingrediente['name_en'])

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
        print(dict_df[pos]['ingredient'])

    for pos in max_similarity_positions_sorted:
        print(dict_df[pos]['ingredient'])

    if similarities[0][max_similarity_positions_sorted[0]] > 0.7:
        compound_data = dict_df[max_similarity_positions_sorted[0]]
        compound_data['max_similarity'] = max_similarity
        collection_ingredientes.update_one({'_id': ingrediente['_id']}, {'$set': {'compounds': [compound_data]}})
        print("Ingrediente actualizado:", ingrediente['name_en'])

    

 

