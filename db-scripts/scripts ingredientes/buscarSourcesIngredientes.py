import pymongo
from pymongo import MongoClient

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')
db = client['tfg']
collection_ingredientes = db['all_ingredients']

# Obtener los diferentes valores del atributo `origin_ISO` en la colección `all_ingredients`
origin_ISO_values = collection_ingredientes.distinct('origin_ISO')

# Imprimir los valores encontrados
print("Diferentes valores de origin_ISO:", origin_ISO_values)
