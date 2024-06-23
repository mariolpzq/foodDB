import pymongo
from pymongo import MongoClient

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')
db = client['tfg']
collection_ingredientes = db['all_ingredients']

# Buscar todos los IDs de los ingredientes que tienen el campo `emissionsID`
ingredientes_con_emissionsID = collection_ingredientes.find({"emissionsID": {"$exists": True}}, {"_id": 1})

# Extraer y mostrar los IDs encontrados
ids = [ingrediente["_id"] for ingrediente in ingredientes_con_emissionsID]

print("IDs de los ingredientes con el campo emissionsID:", ids)
