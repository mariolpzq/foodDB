from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['bedca']

# Nombre del archivo CSV
csv_file = 'bedca/bedca-mongo.csv'

# Abre el archivo CSV y lee los datos
with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        
        if 'category_esp' in row and 'category_en' in row and 'name_esp' in row and 'name_en' in row and 'langual' in row and 'car' in row and 'fiber' in row and 'cal' in row and 'chloride' in row and 'iron' in row and 'pot' in row and 'mag' in row and 'sod' in row and 'phos' in row and 'energy_kcal' in row and 'pro' in row and 'wat' in row and 'cholesterol' in row and 'sug' in row and 'sat' in row and 'trans' in row and 'total_fat' in row:
            
            # Categoría en español (eliminar punto final que pone Google Translate por algún motivo desconocido)
            
            if row['category_esp'].endswith('.'):
                category_esp = row['category_esp'][:-1]
            else:
                category_esp = row['category_esp']
                
            # OMS LIGHTS
            
            oms_lights_salt, oms_lights_sug, oms_lights_total_f, omg_lights_trans = "", "", "", ""
                
            if row['sod'] != '':
                sod = float(row['sod'])/1000 # Pasar de mg a g
                salt = sod * 2.5
                
                if salt <= 0.3 :
                    oms_lights_salt = "green"
                elif 0.3 < salt <= 1.5 :
                    oms_lights_salt = "orange"
                else:
                    oms_lights_salt = "red"
                    
            if row['sug'] != '':
                sug = float(row['sug'])
                
                if sug <= 5 :
                    oms_lights_sug = "green"
                elif 5 < sug <= 22.5 :
                    oms_lights_sug = "orange"
                else:
                    oms_lights_sug = "red"
                    
            if row['total_fat'] != '':
                total_fat = float(row['total_fat'])
                
                if total_fat <= 3 :
                    oms_lights_total_fat = "green"
                elif 3 < total_fat <= 17.5 :
                    oms_lights_total_fat = "orange"
                else:
                    oms_lights_total_fat = "red"
                    
            if row['trans'] != '':
                trans = float(row['trans'])
                
                if trans <= 0.5 :
                    omg_lights_trans = "green"
                elif 0.5 < trans <= 2.0 :
                    omg_lights_trans = "orange"
                else:
                    omg_lights_trans = "red"
                
            # Crear el documento e insertarlo en la colección
                
            document = {
                'name_esp': row['name_esp'],
                'name_en': row['name_en'],
                'langual': row['langual'],
                'origin_ISO': 'ES',
                'source': 'BEDCA',    
                'category_esp': category_esp,
                'category_en': row['category_en'], 
                'edible': float(row['edible'])/10000,            
                'compounds': [],
                'nutritional_info_100g': {
                    'car': float(row['car']) if row['car'] != '' else None,
                    'energy_kcal': float(row['energy_kcal']) if row['energy_kcal'] != '' else None,
                    'energy_kj': round((float(row['energy_kcal'])*4.18),3) if row['energy_kcal'] != '' else None,
                    'pro': float(row['pro']) if row['pro'] != '' else None,
                    'wat': float(row['wat']) if row['wat'] != '' else None,
                    'sug': float(row['sug']) if row['sug'] != '' else None,
                    'fats': {
                    'total_fat': float(row['total_fat']) if row['total_fat'] != '' else None,
                    'sat': float(row['sat']) if row['sat'] != '' else None,
                    'trans': float(row['trans']) if row['trans'] != '' else None,
                    },
                    'fiber': float(row['fiber']) if row['fiber'] != '' else None,
                    'cal': float(row['cal']) if row['cal'] != '' else None,
                    'chloride': float(row['chloride']) if row['chloride'] != '' else None,
                    'iron': float(row['iron']) if row['iron'] != '' else None,
                    'pot': float(row['pot']) if row['pot'] != '' else None,
                    'mag': float(row['mag']) if row['mag'] != '' else None,
                    'sod': float(row['sod']) if row['sod'] != '' else None,
                    'salt': round((float(row['sod'])*2.5),3) if row['sod'] != '' else None,
                    'phos': float(row['phos']) if row['phos'] != '' else None,
                    'cholesterol': float(row['cholesterol']) if row['cholesterol'] != '' else None,
                },
                'oms_lights': {
                    'salt': oms_lights_salt,
                    'sug': oms_lights_sug,
                    'total_fat': oms_lights_total_fat,
                    'trans': omg_lights_trans,
                },
            }
            collection.insert_one(document) 
        else:
            print('No se pudo insertar el documento:', row)
            
            
        
        
      