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

cursor = collection_ingredientes.find({}) # Obtener todos los ingredientes

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

cursor_recetas = collection_recetas.find({}) # Obtener todas las recetas


# Recorremos todas las recetas

print("Recorremos todas las recetas...")

for receta in cursor_recetas: # Recorrer todas las recetas

    ingredientes = receta['ingredients']

    for ingrediente_receta in ingredientes: # Recorrer todos los ingredientes de la receta

        # Codificar el ingrediente de la receta

        mi_ingrediente = ingrediente_receta['ingredient']
        mi_ingrediente_main = model.encode([get_main_ingredient(mi_ingrediente)])
        mi_ingrediente_details = model.encode([get_details(mi_ingrediente)])

        print(ingrediente_receta['ingredient'])

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
            print(dict_df[pos]['name_en'])

        """## 2.2 Identificación de la parte detallada del ingrediente (todo lo que sigue la primera coma)
        Una vez tenemos la coincidencia máxima de ingrediente (en general), miramos la info detallada para intentar acertar al máximo. Usamos la misma metodología, pero esta vez únicamente nos quedamos con el que nos de la descripción más acertada de todas.
        """

        similarities = np.array(cosine_similarity(mi_ingrediente_details.reshape(1, -1), ingredient_details_encoding[max_similarity_positions]))
        sorted_indices = similarities.argsort()[0][::-1]

        # Obtener los alimentos principales que corresponden a los índices ordenados
        max_similarity_positions_sorted = [max_similarity_positions[idx] for idx in sorted_indices]

        print(max_similarity_positions_sorted)

        for pos in max_similarity_positions_sorted:
            print(dict_df[pos]['name_en'])

        """### Resultado

        Y la opción final más parecida, sería la que aparece en este último vector ordenado en la posición 0

        """

        print(dict_df[max_similarity_positions_sorted[0]])

        collection_recetas.update_one(
            {'_id': receta['_id'], 'ingredients.ingredient': mi_ingrediente},
            {'$set': {
                'ingredients.$.ingredientID': dict_df[max_similarity_positions_sorted[0]]['_id'],
                'ingredients.$.max_similarity': max_similarity
            }}
        )

