import pymongo
from pymongo import MongoClient

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')
db = client['tfg']
collection = db['food.com']

# Obtener las recetas de la colección
recetas_cursor = collection.find({})

for receta in recetas_cursor:
    # Iterar sobre cada receta
    for i, ingrediente in enumerate(receta['ingredients']):
        # Renombrar el campo 'name' a 'ingredient'
        receta['ingredients'][i]['ingredient'] = receta['ingredients'][i].pop('name')

    # Actualizar la receta en la colección
    collection.update_one({'_id': receta['_id']}, {'$set': {'ingredients': receta['ingredients']}})
    print(f"Receta actualizada: {receta['_id']}")
