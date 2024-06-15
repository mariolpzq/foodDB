from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['abuela']

# Buscar los difernetes valores de origin_ISO en todas las recetas

cuisines = set()

for doc in collection.find({}):
    if 'origin_ISO' in doc:
        cuisines.add(doc['origin_ISO'])

print(cuisines)
print(len(cuisines))
print("Búsqueda completada.")
