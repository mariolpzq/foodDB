from pymongo import MongoClient

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['abuela']

# Clasificación de categorías
entrantes = {'botanas', 'ensaladas', 'bebidas', 'salsas'}
platos_principales = {
    'Receta sin gluten', 'Recetas japonesas', 'Recetas para San Valentín', 'Recetas cordobesas', 'Recetas amazónicas de Venezuela',
    'Recetas asturianas', 'guisados', 'Receta sin azúcar', 'temporada y navidad', 'Recetas mexicanas', 'Recetas chilenas',
    'Recetas chinas', 'Recetas al microondas', 'Recetas yucatecas', 'Recetas para Semana Santa', 'Recetas antioqueñas',
    'Recetas caraqueñas', 'desayuno y almuerzos', 'Recetas chiapanecas', 'Recetas andaluzas', 'Recomendada para veganos',
    'Recetas argentinas', 'Recetas gallegas', 'Recetas al vapor', 'Recetas colombianas', 'Recetas para Año Nuevo', 'antojitos',
    'Recetas bogotanas', 'Recetas tabasqueñas', 'carne de res', 'tacos', 'Recetas vascas', 'Recetas llaneras', 'Recetas de Piura',
    'Recetas sinaloenses', 'Recomendada para vegetarianos', 'Recomendada para perder peso', 'vegetarianos', 'Recetas españolas',
    'Recetas indias', 'Recetas de Chubut', 'cuaresma', 'cerdo', 'Receta sin sal', 'Recetas para Navidad', 'Recetas venezolanas',
    'Recetas poblanas', 'Recetas al horno', 'Recetas riojanas', 'Recetas valencianas', 'Receta sin lactosa', 'Recetas amazónicas de Perú',
    'vigilia', 'pastas', 'Recetas italianas', 'Recetas catalanas', 'navidad', 'queso', 'Recetas peruanas', 'Recetas de Buenos Aires',
    'Recetas veracruzanas', 'pollo'
}
postres = {'panes y galletas', 'postres', 'frutas'}

# Función para determinar la nueva categoría basada en la subcategoría
def determinar_categoria(subcategories):
    for subcategory in subcategories:
        if subcategory in entrantes:
            return 'entrante'
        elif subcategory in postres:
            return 'postre'
    for subcategory in subcategories:
        if subcategory in platos_principales:
            return 'plato principal'
    return 'otros' if subcategories else ''

# Actualizar documentos en la colección
for doc in collection.find({}):
    if 'category' in doc and doc['category']:
        subcategories = doc['category'] if isinstance(doc['category'], list) else [doc['category']]
        
        new_category = determinar_categoria(subcategories)
        
        # Actualizar el documento
        collection.update_one(
            {'_id': doc['_id']},
            {
                '$set': {'subcategory': subcategories, 'category': new_category}
            }
        )

        print(f"Receta actualizada: {doc['_id']}")

print("Actualización completada.")
