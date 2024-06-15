from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['abuela']

# Contar cuántas recetas tienen más de un elemento en el array category
count = 0

for doc in collection.find({}):
    if 'subcategory' in doc and isinstance(doc['subcategory'], list) and len(doc['subcategory']) > 1:
        count += 1

print(f'Número de recetas con más de un elemento en el array category: {count}')