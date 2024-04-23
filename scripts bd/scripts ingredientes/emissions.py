from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['emissions']

# Nombre del archivo CSV
csv_file = 'emissions/food_production.csv'

# Abre el archivo CSV y lee los datos
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
     
        document = {
                'id_alimento': "",
                'name_esp': row['name_esp'],
                'name_en': row['name_en'],
                'land_use_change': float(row['land_use_change']) if row['land_use_change'] != '' else None,
                'animal_feed': float(row['animal_feed']) if row['animal_feed'] != '' else None,
                'farm': float(row['farm']) if row['farm'] != '' else None,
                'processing': float(row['processing']) if row['processing'] != '' else None,
                'transport': float(row['transport']) if row['transport'] != '' else None,
                'packaging': float(row['packaging']) if row['packaging'] != '' else None,
                'retail': float(row['retail']) if row['retail'] != '' else None,
                'total_emissions': float(row['total_emissions']) if row['total_emissions'] != '' else None,
                'euto' : {
                    'euto_1000kcal': float(row['euto_1000kcal']) if row['euto_1000kcal'] != '' else None,
                    'euto_100g_protein': float(row['euto_protein']) if row['euto_protein'] != '' else None,
                    'euto_kilogram': float(row['euto_kilogram']) if row['euto_kilogram'] != '' else None,                   
                },
                'withdrawals': {
                    'withdrawals_1000kcal': float(row['withdrawals_1000kcal']) if row['withdrawals_1000kcal'] != '' else None,
                    'withdrawals_100g_protein': float(row['withdrawals_protein']) if row['withdrawals_protein'] != '' else None,
                    'withdrawals_kilogram': float(row['withdrawals_kilogram']) if row['withdrawals_kilogram'] != '' else None,
                },
                'greenhouse': {
                    'greenhouse_1000kcal': float(row['greenhouse_1000kcal']) if row['greenhouse_1000kcal'] != '' else None,
                    'greenhouse_100g_protein': float(row['greenhouse_protein']) if row['greenhouse_protein'] != '' else None,
                },
                'land_use': {
                    'land_use_1000kcal': float(row['land_use_1000kcal']) if row['land_use_1000kcal'] != '' else None,
                    'land_use_100g_protein': float(row['land_use_protein']) if row['land_use_protein'] != '' else None,
                    'land_use_kilogram': float(row['land_use_kilogram']) if row['land_use_kilogram'] != '' else None,
                },
                'scarcity_water_use': {
                    'scarcity_water_use_1000kcal': float(row['scarcity_water_use_1000kcal']) if row['scarcity_water_use_1000kcal'] != '' else None,
                    'scarcity_water_use_100g_protein': float(row['scarcity_water_use_protein']) if row['scarcity_water_use_protein'] != '' else None,
                    'scarcity_water_use_kilogram': float(row['scarcity_water_use_kilogram']) if row['scarcity_water_use_kilogram'] != '' else None,
                },
            }
        collection.insert_one(document) 

            
        