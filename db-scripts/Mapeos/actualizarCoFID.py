import pymongo
from pymongo import MongoClient

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')
db = client['tfg']
collection_ingredientes = db['cofid']

# Paso 1: Obtener los documentos de la colección
documentos_cursor = collection_ingredientes.find({})

for documento in documentos_cursor:
    # Paso 2: Verificar si el campo `compounds` es un objeto en lugar de un array
    if isinstance(documento.get('compounds'), dict):
        # Paso 3: Convertir el campo `compounds` en un array con un solo elemento
        compounds_objeto = documento['compounds']
        documento['compounds'] = [compounds_objeto]
        # Paso 4: Actualizar el documento en la colección con el campo `compounds` convertido en un array
        collection_ingredientes.update_one({'_id': documento['_id']}, {'$set': {'compounds': documento['compounds']}})
        print(f"Documento actualizado: {documento['_id']}")

print("Limpieza completada.")