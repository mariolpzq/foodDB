import pymongo

from pymongo import MongoClient


# Carga de la base de datos 

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['emissions']

# Actualizar todos los documentos en la colección y eliminar el campo "id_alimento"
collection.update_many({}, {"$unset": {"id_alimento": ""}})