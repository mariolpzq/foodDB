import pymongo
from pymongo import MongoClient
from concurrent.futures import ThreadPoolExecutor

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection_recipe1m = db['recipe1m']
collection_recipeNLG = db['recipeNLG']

# Asegurarse de que los campos 'url' están indexados
collection_recipe1m.create_index('url')
collection_recipeNLG.create_index('url')

def process_recipe(receta):
    # Verificar si la receta ya tiene el campo recipenlg_id
    if 'recipeNLG_id' in receta:
        print(f"La receta {receta['_id']} ya tiene el campo recipeNLG_id, se omite.")
        return
    
    receta_url = receta.get('url')
    if receta_url:
    # Quitamos el prefijo http:// si existe
        normalized_url = receta_url.replace('http://', '')

        receta_NLG = collection_recipeNLG.find_one({'url': normalized_url})
        if receta_NLG:

            collection_recipeNLG.update_one(
                {'_id': receta_NLG['_id']},
                {'$set': {'recipe1m_id': receta['_id']}}
            )

            collection_recipe1m.update_one(
                {'_id': receta['_id']},
                {'$set': {'recipeNLG_id': receta_NLG['_id']}}
            )
            print(f"Recetas actualizadas: recipe1m_id en recipeNLG y recipeNLG_id en recipe1m para URL: {normalized_url}")

# Obtenemos las recetas de la colección recipe1m
recetas_cursor = collection_recipe1m.find({})

# Utilizamos ThreadPoolExecutor para procesar recetas en paralelo
with ThreadPoolExecutor(max_workers=10) as executor:
    executor.map(process_recipe, recetas_cursor)

print("Actualización completa.")
