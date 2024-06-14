from pymongo import MongoClient


MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['recipeNLG']


# Buscar recetas con la misma URL
pipeline = [
    {"$group": {"_id": "$url", "count": {"$sum": 1}}},
    {"$match": {"count": {"$gt": 1}}}
]

duplicates = list(collection.aggregate(pipeline))

# Imprimir las URLs de las recetas duplicadas
if duplicates:
    print("Se encontraron recetas con la misma URL:")
    for duplicate in duplicates:
        print(duplicate['_id'])
else:
    print("No se encontraron recetas con la misma URL.")