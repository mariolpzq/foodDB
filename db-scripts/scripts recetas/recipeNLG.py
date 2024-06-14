from pymongo import MongoClient
import csv

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['recipeNLG']

# Nombre del archivo CSV
csv_file = 'recipeNLG_subset2.csv'

# Obtener el último índice de la receta insertada en la base de datos
last_index = collection.count_documents({})
print("Último índice insertado:", last_index)

# Abre el archivo CSV y lee los datos a partir del último índice
with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)

    first_index = int(next(reader)['index'])  # Obtiene el primer índice del archivo
    print("Primer índice del archivo:", first_index)

    if last_index == 0:
        print("No hay recetas en la base de datos")
        last_index = first_index

    # Itera hasta el último índice insertado
    for i in range(first_index, last_index):  # Salta las recetas ya insertadas
        next(reader)

    # Colección de documentos para la inserción en lotes
    documentos = []

    # Itera a partir del último índice
    for row in reader:
        ingredients = [ingredient.strip().strip('"') for ingredient in row['ingredients'].strip("[]").split(',')]
        steps = [step.strip().strip('"') for step in row['directions'].strip("[]").split(',')]
        NER = [ner.strip().strip('"') for ner in row['NER'].strip("[]").split(',')]

        nuevo_documento = {
            'title': row['title'],
            'url': row['link'],
            'source': 'RecipeNLG',
            'n_ingredients': len(ingredients),
            'ingredients': ingredients,
            'n_steps': len(steps),
            'steps': steps,
            'NER': NER
        }

        documentos.append(nuevo_documento)

        # Inserta en lotes de 10000 documentos
        if len(documentos) == 10000:
            collection.insert_many(documentos)
            print(collection.count_documents({}), "recetas insertadas correctamente")
            documentos = []

    # Inserta los documentos restantes, si hay menos de 10000
    if documentos:
        collection.insert_many(documentos)
        print(collection.count_documents({}), "recetas insertadas correctamente")
