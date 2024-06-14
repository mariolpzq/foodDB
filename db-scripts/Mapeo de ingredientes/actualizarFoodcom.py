import pymongo
from pymongo import MongoClient

# Carga de la base de datos 
MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['food.com']

# Paso 1: Obtener las recetas de la colección de recetas
recetas_cursor = collection.find({})

for receta in recetas_cursor:
    # Paso 2: Iterar sobre cada receta
    for i, ingrediente in enumerate(receta['ingredients']):
        # Paso 3: Verificar si el ingrediente es un diccionario y contiene el campo `ingredientID`
        if isinstance(ingrediente, dict) and 'ingredientID' in ingrediente:
            # Paso 4: Eliminar el campo `ingredientID`
            del receta['ingredients'][i]['ingredientID']

    # Paso 5: Actualizar la receta en la colección de recetas con el campo `ingredientID` eliminado
    collection.update_one({'_id': receta['_id']}, {'$set': {'ingredients': receta['ingredients']}})
    print(f"Receta actualizada: {receta['_id']}")
