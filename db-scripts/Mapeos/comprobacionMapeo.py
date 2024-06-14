import pymongo
from pymongo import MongoClient

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'
client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')
db = client['tfg']
collection = db['food.com']

# Contador de documentos sin ningún ingrediente con 'ingredientID'
contador_documentos_sin_ingredientID = 0
# Lista para almacenar los valores de 'name_en' de los documentos problemáticos
recetas_sin_ingredientID = []

# Obtener documentos de la colección
documentos_cursor = collection.find({})

for documento in documentos_cursor:
    # Bandera para comprobar si todos los ingredientes no tienen 'ingredientID'
    ningun_ingredientID = True
    
    for ingrediente in documento['ingredients']:
        # Comprobar si el ingrediente tiene el campo 'ingredientID'
        if 'ingredientID' in ingrediente:
            ningun_ingredientID = False
            break  # No necesitamos seguir comprobando este documento
    
    # Incrementar el contador y agregar 'name_en' a la lista si no hay 'ingredientID' en ningún ingrediente
    if ningun_ingredientID:
        contador_documentos_sin_ingredientID += 1
        recetas_sin_ingredientID.append(documento.get('title'))

print(f"Número de recetas sin ningún ingrediente con 'ingredientID' (pendientes de mapear): {contador_documentos_sin_ingredientID}")
"""
print("Títulos de esas recetas:")
for titulo in recetas_sin_ingredientID:
    print(titulo)
"""