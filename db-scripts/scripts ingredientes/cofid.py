from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['cofid']

# Nombre del archivo CSV
csv_file = 'cofid/cofid-mongo.csv'

# Abre el archivo CSV y lee los datos
with open(csv_file, 'r') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:
        #if 'category_esp' in row and 'category_en' in row and 'name_esp' in row and 'name_en' in row and 'car' in row and 'fiber' in row and 'energy_kcal' in row and 'pro' in row and 'wat' in row and 'cholesterol' in row and 'sug' in row and 'sat' in row and 'trans' in row and 'total_fat' in row:
            
            # Categoría en español (eliminar punto final que pone Google Translate por algún motivo desconocido)
            
            if row['category_esp'].endswith('.'):
                category_esp = row['category_esp'][:-1]
            else:
                category_esp = row['category_esp']
                
            # OMS LIGHTS
            
            oms_lights_salt, oms_lights_sug, oms_lights_total_f, omg_lights_trans = "", "", "", ""
                
                
            # Este dataset no contiene información relativa a la cantidad de sodio, por lo que no se puede calcular el semáforo de sal.
            # ACTUALIZACIÓN: el dataset sí que contenía esta información. El script para actualizar la colección es inorganicosCofid.py
                    
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
                'origin_ISO': 'GBR',
                'source': 'CoFID',    
                'category_esp': category_esp,
                'category_en': row['category_en'], 
                'edible': "", # No se dispone de esta información          
                'compounds': [],
                'nutritional_info_100g': {
                    'car': float(row['car']) if row['car'] != '' else None,
                    'energy_kcal': float(row['energy_kcal']) if row['energy_kcal'] != '' else None,
                    'energy_kj': float(row['energy_kj']) if row['energy_kj'] != '' else None,
                    'pro': float(row['pro']) if row['pro'] != '' else None,
                    'wat': float(row['wat']) if row['wat'] != '' else None,
                    'sug': float(row['sug']) if row['sug'] != '' else None,
                    'fats': {
                        'total_fat': float(row['total_fat']) if row['total_fat'] != '' else None,
                        'sat': float(row['sat']) if row['sat'] != '' else None,
                        'trans': float(row['trans']) if row['trans'] != '' else None,
                    },
                    'fiber': float(row['fiber']) if row['fiber'] != '' else None,
                    'cal': "", # No se dispone de esta información
                    'chloride': "", # No se dispone de esta información
                    'iron': "", # No se dispone de esta información
                    'pot': "", # No se dispone de esta información
                    'mag': "", # No se dispone de esta información
                    'sod': "", # No se dispone de esta información
                    'salt': "", # No se dispone de esta información
                    'phos': "", # No se dispone de esta información
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
        #else:
        #    print('No se pudo insertar el documento:', row)
            
            
        
        
      