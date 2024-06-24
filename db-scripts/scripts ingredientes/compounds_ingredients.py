from pymongo import MongoClient
import csv
import pandas as pd

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

# Selección de la base de datos y las colecciones
db = client['tfg']
ingredientes = db['all_ingredients_with_compounds']
compounds = db['compounds']

# Iterar sobre cada documento en la colección de ingredientes
for ingrediente in ingredientes.find():
    # Obtener el nombre del ingrediente en inglés y convertirlo a minúsculas
    name_en = ingrediente['name_en'].lower().split(',')[0]
    
    # Iterar sobre cada documento en la colección de compuestos
    for compound in compounds.find():
        # Verificar si el nombre del compuesto está en el nombre del ingrediente
        if compound['ingredient'].lower() in name_en:
            # Añadir el compuesto al campo 'compounds' del ingrediente
            compounds_list = ingrediente.get('compounds', [])
            compounds_list.append({k: v for k, v in compound.items() if k != '_id'})
            # Actualizar el documento del ingrediente con la lista de compuestos
            ingredientes.update_one({'_id': ingrediente['_id']}, {'$set': {'compounds': compounds_list}})
            print(f"Compuesto {compound['ingredient']} añadido a {name_en}")
            break
