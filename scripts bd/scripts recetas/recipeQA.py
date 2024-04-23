import pymongo
import json
from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['recipeQA']

# Cargar datos desde el archivo JSON
with open('recipeQA/recipes-val.json', 'r') as archivo_json:
    datos = json.load(archivo_json)

# Procesar cada documento y realizar la inserción
for documento in datos:
    
    documento_pasos = 'recipeQA/steps/' + documento['steps']
    
    with open(documento_pasos, 'r') as archivo_json:
        documento_pasos = json.load(archivo_json)
    
    pasos_conglomerados = []
    
    for i, paso in enumerate(documento_pasos['steps']):
        nuevo_paso = {
            'title': paso['title'],
            'body': paso['body'],
            'id': paso['id'],
            'image_urls': paso['image_urls'],
            'images': paso['images'],
            'video_urls': paso['video_urls'],
            'videos': paso['videos'],
        }
                      
        pasos_conglomerados.append(nuevo_paso)       
 
    nuevo_documento = {
        'title': documento['name'],
        'URL': documento['url'],
        'source': 'RecipeQA',
        'thumbnail': documento['thumbnail'], # Campo presente únicamente en RecipeQA
        'licence': documento['licence'], # Campo presente únicamenteen RecipeQA
        'language_ISO': 'EN',
        'origin_ISO' : '', 
        'n_diners': '',
        'category': documento['category'],
        'subcategory': '',
        'minutes': '',
        'n_ingredients': '',
        'ingredients': '', 
        'steps_file': documento['steps'], # Campo presente únicamente en RecipeQA     
        'n_steps': documento['step_size'],
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
            'energy':'',
            'car': '',
            'pro': '',
            'fat': '',         
            'sat': '',
            'trans': '', 
            'salt': '',
            'sug': '',
            'fiber': '', 
        },
        'nutritional_info_PDV': {     
            'energy': '',     
            'fat': '', 
            'car': '',
            'pro': '',
            'sat': '',
            'salt': '', 
            'sug': '',
        },
        'FSA_lights_per100g': {
            'fat':'',
            'salt': '',
            'sat': '',
            'sug': '',
            'energy': '',
            'sod': '',
            'fiber': '',
            'pro': '',
        },
        'OMS_lights_per100g': {
            'fat': '',
            'trans': '', 
            'salt': '',
            'sug': '',            
        },

    }
    
    collection.insert_one(nuevo_documento)
    
print('Documentos insertados correctamente')
        
        