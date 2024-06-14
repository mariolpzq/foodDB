import pymongo
from pymongo import MongoClient

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')
db = client['tfg']
collection = db['abuela']

# Obtener documentos de la colección
documentos_cursor = collection.find({})

for documento in documentos_cursor:
    # Iterar sobre cada documento
    for i, ingrediente in enumerate(documento['ingredients']):
        # Modificar el contenido del array 'ingredients'
        documento['ingredients'][i] = {'ingredient': ingrediente}

    # Actualizar el documento en la colección
    collection.update_one({'_id': documento['_id']}, {'$set': {'ingredients': documento['ingredients']}})
    print(f"Documento actualizado: {documento['_id']}")