from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['abuela']

# Buscar los diferentes valores de category en todas las recetas

categories = set()

for doc in collection.find({}):
    if 'category' in doc:
        for category in doc['category']:
            categories.add(category)

print(categories)
print(len(categories))
print("Búsqueda completada.")
