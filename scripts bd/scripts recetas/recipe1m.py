import pymongo
import json
from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['recipe1m']
collection_originales = db['recipe1m_originals']

# Cargar datos desde el archivo JSON
with open('recipe1M/recipes_with_nutritional_info.json', 'r') as archivo_json:
    datos = json.load(archivo_json)
    
    
# Procesar cada documento y realizar la inserción
for documento in datos:
    
    url = documento['url']
    original_doc = collection_originales.find_one({'url': url})
    
    ingredientes_originales = []
    
    if original_doc:
        ingredientes_originales = original_doc['ingredients']  
    """
    ingredientes_originales = []
    
    for receta in datos_originales:
        if receta['url'] == documento['url']:
            ingredientes_originales = receta['ingredients']
            break

    """
    
    print("Título:", documento['title'])
    #print("Ingredientes originales:", ingredientes_originales)
    
    ingredientes_conglomerados = []
    
    for i, ingrediente in enumerate(documento['ingredients']):

        ingrediente = {
            'original_ingredient': ingredientes_originales[i]['text'] if ingredientes_originales else '',
            'ingredient': ingrediente['text'],
            'id': '',
            'quantity': documento['quantity'][i]['text'],
            'unit': documento['unit'][i]['text'],
            'weight': documento['weight_per_ingr'][i],
            'nutr_per_ingredient': documento['nutr_per_ingredient'][i]
        }

        ingredientes_conglomerados.append(ingrediente)
        
    pasos_conglomerados = []
    
    for i, step in enumerate(documento['instructions']):
        step = {
            'step': step['text'],
            'image': '',
        }
        
        pasos_conglomerados.append(step)
        
    # Cálculo de los semáforos nutricionales de la OMS
    
    oms_lights_salt, oms_lights_sug, oms_lights_fat = "", "", ""
        
    if documento['nutr_values_per100g']['salt'] != '':
            salt = float(documento['nutr_values_per100g']['salt'])
            
            if salt <= 0.3 :
                oms_lights_salt = "green"
            elif 0.3 < salt <= 1.5 :
                oms_lights_salt = "orange"
            else:
                oms_lights_salt = "red"
                
    if documento['nutr_values_per100g']['sugars'] != '':
        sug = float(documento['nutr_values_per100g']['sugars'])
        
        if sug <= 5 :
            oms_lights_sug = "green"
        elif 5 < sug <= 22.5 :
            oms_lights_sug = "orange"
        else:
            oms_lights_sug = "red"
                
    if documento['nutr_values_per100g']['fat'] != '':
        fat = float(documento['nutr_values_per100g']['fat'])
        
        if fat <= 3 :
            oms_lights_fat = "green"
        elif 3 < fat <= 17.5 :
            oms_lights_fat = "orange"
        else:
            oms_lights_fat = "red"
            
    # Este dataset no proporciona información sobre el contenido de grasas trans de 100 gramos de receta
                    
        
    # Seleccionar campos específicos y reordenarlos
    nuevo_documento = {
        'title': documento['title'],
        'URL': documento['url'],
        'source': 'Recipe1M',
        'language_ISO': 'EN',
        'origin_ISO' : '', # Gastronomía de origen de la receta
        'n_diners': '',
        'category': '',
        'subcategory': '',
        'minutes': '',
        'n_ingredients': ingredientes_conglomerados.__len__(),  
        'ingredients': ingredientes_conglomerados,         
        'n_steps': pasos_conglomerados.__len__(),
        'steps': pasos_conglomerados,
        'images': [],
        'interactions': [{
            'user_id': '',
            'date': '',
            'rating': '',
            'review': ''
        }],
        'aver_rate': '',
        'num_interactions': '', # Número de reviews de la receta
        'nutritional_info_100g': {
            'energy': documento['nutr_values_per100g']['energy'],
            'car': '', # Necesario calcularlo a través de los valores de cada uno de los ingredientes multiplicados por su peso
            'pro': documento['nutr_values_per100g']['protein'],
            'fat': documento['nutr_values_per100g']['fat'],         
            'sat': documento['nutr_values_per100g']['saturates'],
            'trans': '',  # Necesario calcularlo a través de los valores de cada uno de los ingredientes multiplicados por su peso
            'salt': documento['nutr_values_per100g']['salt'],
            'sug': documento['nutr_values_per100g']['sugars'],
            'fiber': '', # Necesario calcularlo a través de los valores de cada uno de los ingredientes multiplicados por su peso
        },
        'nutritional_info_PDV': { # Porcentaje del valor diario de referencia (PDV) por 100 gramos - basado en una dieta de 2000 kcal    
            'energy': round((documento['nutr_values_per100g']['energy']/2000) * 100, 2),     
            'fat': round((float(documento['nutr_values_per100g']['fat'])/66) * 100, 2), # 66 gramos de grasas al día
            'car': '', # Necesario calcular en primer lugar los carbohidratos
            'pro': round((float(documento['nutr_values_per100g']['protein'])/50) * 100, 2), # 50 gramos de proteínas al día
            'sat': round((float(documento['nutr_values_per100g']['saturates'])/22) * 100, 2), # 22 gramos de grasas saturadas al día
            'salt': round((float(documento['nutr_values_per100g']['salt'])/5) * 100, 2), # 5 gramos de sal al día (2 gramos de sodio)
            'sug': round((float(documento['nutr_values_per100g']['sugars'])/50) * 100, 2), # 50 gramos de azúcares al día
        },
        'FSA_lights_per100g': {
            'fat': documento['fsa_lights_per100g']['fat'],
            'salt': documento['fsa_lights_per100g']['salt'],
            'sat': documento['fsa_lights_per100g']['saturates'],
            'sug': documento['fsa_lights_per100g']['sugars'],
            # Los campos que están vacíos dependen de la implemetación de la FSA que se haya realizado
            'energy': '',
            'sod': '',
            'fiber': '',
            'pro': '',
        },
        'OMS_lights_per100g': {
            'fat': oms_lights_fat,
            'trans': '', # No se dispone de esta información
            'salt': oms_lights_salt,
            'sug': oms_lights_sug,            
        },

    }
    
    # Insertar el nuevo documento en la colección
    collection.insert_one(nuevo_documento)
    print(f"Inserciones totales: {collection.count_documents({})}")

print("Inserción completada.")


