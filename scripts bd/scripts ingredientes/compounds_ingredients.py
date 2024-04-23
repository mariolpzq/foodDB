from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
ingredientes = db['all_ingredients_with_compounds']
compounds = db['compounds']

for ingrediente in ingredientes.find():
    name_en = ingrediente['name_en'].lower().split(',')[0]
    
    for compound in compounds.find():
        if compound['ingredient'].lower() in name_en:
            compounds_list = ingrediente.get('compounds', [])
            compounds_list.append({k: v for k, v in compound.items() if k != '_id'})
            ingredientes.update_one({'_id': ingrediente['_id']}, {'$set': {'compounds': compounds_list}})
            print(f"Compuesto {compound['ingredient']} añadido a {name_en}")
            break