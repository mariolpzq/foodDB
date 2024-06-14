import pymongo
from pymongo import MongoClient

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')
db = client['tfg']
collection_ingredientes = db['all_ingredients']

# Paso 1: Obtener los documentos de la colección con el campo `source` igual a "FDC"
documentos_cursor = collection_ingredientes.find({'source': 'FDC'})

for documento in documentos_cursor:
    # Paso 2: Actualizar el campo `source` de "FDC" a "USDA"
    collection_ingredientes.update_one({'_id': documento['_id']}, {'$set': {'source': 'USDA'}})
    print(f"Documento actualizado: {documento['_id']}")

print("Actualización completada.")
