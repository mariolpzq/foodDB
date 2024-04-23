from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['abuela']

# Nombre del archivo CSV
csv_file = 'RecetasDeLaAbuela/main.csv'

with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        
        print("Insertando receta", row['Nombre'])
        
        lista_ingredientes = [ingredient.strip().strip('[]') for ingredient in row['Ingredientes'].split(',')]
        
        lista_pasos = [paso.strip().strip('[]') for paso in row['Pasos'].split('.') if paso.strip() != '']
        
        
        if row['Duracion'] == '' or len(row['Duracion']) > 5:
            continue
        else:
            duration = row['Duracion']
            try:
                hours, minutes = duration.split(':')
                total_minutes = int(hours) * 60 + int(minutes)
            except:
                total_minutes = ''
        
        valoracion_y_votos = row['Valoracion y Votos']
        if valoracion_y_votos != '':
            valoracion_string = valoracion_y_votos.split(':')[1].split('(')[0].strip()
            aver_rate = float(valoracion_string.replace(',', '.'))
            try:
                num_interactions = int(valoracion_y_votos.split('(')[1].split(' ')[0])
            except:
                num_interactions = 0
        else:
            aver_rate = ''
            num_interactions = 0
        
        dietary_preferences = [preference.strip() for preference in row['Valor nutricional'].split(',')]
        
        categoria = row['Categoria']
        categoria = categoria.replace('[', '').replace(']', '').replace("'", "")
        categoria = categoria.split(', ')
        
        
        comensales = row['Comensales']
        if comensales != '':
            try:
                n_diners = int(comensales.split()[0])
            except:
                n_diners = ''
        else:
            n_diners = ''
        
        documento = {
            "title": row['Nombre'],
            'url': row['URL'],
            'descripcion': row['Contexto'],
            'source': 'Recetas de la abuela',
            'language_ISO': 'ES',
            'origin_ISO' : row['Pais'], # Gastronomía de origen,
            'n_diners': n_diners,
            'dificultad': row['Dificultad'], # Dificultad de la receta
            'category': categoria,
            'subcategory': '',
            'minutes': int(total_minutes),
            'n_ingredients': len(lista_ingredientes),
            'ingredients' : lista_ingredientes,
            'n_steps': len(lista_pasos),
            'steps' : lista_pasos,
            'images': [],
            'interactions': '',
            'aver_rate': aver_rate,
            'num_interactions': num_interactions, # Número de reviews de la receta
            'tags' : [],
            'num_tags': '',
            'dietary_preferences' : dietary_preferences,
        }
        
        try:
            collection.insert_one(documento)
            print(collection.count_documents({}), "recetas insertadas correctamente")
        except Exception as e:
            print("Error insertando:", documento["title"])
            print("Error message:", str(e))


                
          
        