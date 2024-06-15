from pymongo import MongoClient

# Conexión a la base de datos MongoDB
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['abuela']

# Set para almacenar valores únicos de dietary_preferences
dietary_preferences_set = set()

# Recorrer todos los documentos en la colección
for doc in collection.find({}):
    if 'dietary_preferences' in doc:
        for preference in doc['dietary_preferences']:
            dietary_preferences_set.add(preference)

# Convertir el set a lista para un mejor manejo si es necesario
dietary_preferences_list = list(dietary_preferences_set)

# Imprimir los valores únicos de dietary_preferences
print("Valores únicos de dietary_preferences en toda la colección:")
for preference in dietary_preferences_list:
    print(preference)

print(f"Total de valores únicos: {len(dietary_preferences_list)}")
