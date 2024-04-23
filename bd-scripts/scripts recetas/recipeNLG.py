from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['recipenlg']

# Nombre del archivo CSV
csv_file = 'recipeNLG/recipeNLG.csv'

# Abre el archivo CSV y lee los datos
with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for row in reader:
        
        recipe1m = db['recipe1m_originals']
        
        existing_recipe = recipe1m.find_one({'url': 'http://' + row['link']})
        if existing_recipe:
            recipe1M_ID = existing_recipe['_id']
        else:
            recipe1M_ID = ''
        
        ingredients = [ingredient.strip().strip('"') for ingredient in row['ingredients'].strip("[]").split(',')]
        steps = [step.strip().strip('"') for step in row['directions'].strip("[]").split(',')]
        NER = [ner.strip().strip('"') for ner in row['NER'].strip("[]").split(',')]
        
        nuevo_documento = {
            'title': row['title'],
            'url': row['link'],
            'source': 'RecipeNLG',
            'recipe1M_ID': recipe1M_ID, # ID de la receta en la colección Recipe1M
            'n_ingredients': ingredients.__len__(),
            'ingredients': ingredients,
            'n_steps': steps.__len__(),
            'steps': steps,
            'NER': NER
        }
         
        collection.insert_one(nuevo_documento) 
        print(collection.count_documents({}), "recetas insertadas correctamente")