import pymongo

from pymongo import MongoClient


# Carga de la base de datos 

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['recipe1m']


# Obtenemos las recetas de la colección de recetas
recetas_cursor = collection.find({})

for receta in recetas_cursor:
    # Iteramos sobre cada receta
    for i, ingrediente in enumerate(receta['ingredients']):
        #Comprobamos si el ingrediente es una cadena y convertirlo a un diccionario si es necesario
        if isinstance(ingrediente, dict) and 'id' in ingrediente:
            del ingrediente['id']  # Eliminar el campo 'id' si existe
            receta['ingredients'][i] = ingrediente  # Actualizar el ingrediente en la lista de ingredientes


    # Actualizo la receta en la colección de recetas con los cambios realizados
    collection.update_one({'_id': receta['_id']}, {'$set': {'ingredients': receta['ingredients']}})
    collection.update_many({'_id': receta['_id']}, {'$rename': {'URL': 'url'}})
                        
    print(f"Receta actualizada: {receta['_id']}")
