from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['food.com_interactions']

# Nombre del archivo CSV
csv_file = 'Food.com/RAW_interactions.csv'

# Abre el archivo CSV y lee los datos
with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    
    for row in reader:
        
        nuevo_documento = {
            'user_id': row['user_id'],
            'recipe_id': row['recipe_id'],
            'date': row['date'],
            'rating': int(row['rating']),
            'review': row['review']
        }
        
        collection.insert_one(nuevo_documento)
            
            
            