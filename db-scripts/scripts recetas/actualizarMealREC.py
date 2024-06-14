from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['mealrec']

# Definir los pasos constantes a buscar
constant_steps = ["Prep", "Cook", "Ready In"]

# Iterar sobre los documentos en la colección
for doc in collection.find({}):
    if 'steps' in doc and len(doc['steps']) >= 6:
        steps = doc['steps']
        
        if steps[0] == constant_steps[0] and steps[2] == constant_steps[1] and steps[4] == constant_steps[2]:
            # Extraer el tiempo total del paso "Ready In"
            total_time = steps[5]
            
            # Eliminar los primeros seis pasos
            updated_steps = steps[6:]
            
            # Actualizar el documento
            collection.update_one(
                {'_id': doc['_id']},
                {
                    '$set': {
                        'minutes': total_time,
                        'steps': updated_steps,
                        'n_steps': len(updated_steps)
                    }
                }
            )
            print(f"Documento con _id {doc['_id']} actualizado correctamente.")

print("Actualización completada.")
