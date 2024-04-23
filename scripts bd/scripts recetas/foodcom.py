from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['food.com']

# Nombre del archivo CSV
csv_file = 'Food.com/RAW_recipes_util.csv'

# Abre el archivo CSV y lee los datos
with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file, delimiter=';')
    for row in reader:       
               
        nutritional_info = [nutritional_info.strip().strip("'") for nutritional_info in row['nutrition'].strip("[]").split(',')] # ['fat', 'sugar', 'salt', 'protein', 'saturated_fat'...]
        
        energy = float(nutritional_info[0])
        
        energy_PDV = energy/2000*100
        fat_PDV = float(nutritional_info[1])
        sug_PDV = float(nutritional_info[2])
        salt_PDV = float(nutritional_info[3])/0.4
        pro_PDV = float(nutritional_info[4])
        sat_PDV = float(nutritional_info[5])
        car_PDV = float(nutritional_info[6])
        
        fat = fat_PDV*66/100
        sug = sug_PDV*50/100
        salt = salt_PDV*5/100
        pro = pro_PDV*50/100
        sat = sat_PDV*22/100
        car = car_PDV*260/100
        
        # Cálculo de los semáforos nutricionales de la OMS
        
        oms_lights_salt, oms_lights_sug, oms_lights_fat = "", "", ""
            
      
        if salt <= 0.3 :
            oms_lights_salt = "green"
        elif 0.3 < salt <= 1.5 :
            oms_lights_salt = "orange"
        else:
            oms_lights_salt = "red"
                    
                  
        if sug <= 5 :
            oms_lights_sug = "green"
        elif 5 < sug <= 22.5 :
            oms_lights_sug = "orange"
        else:
            oms_lights_sug = "red"
                    
      
        if fat <= 3 :
            oms_lights_fat = "green"
        elif 3 < fat <= 17.5 :
            oms_lights_fat = "orange"
        else:
            oms_lights_fat = "red"
            
        # Este dataset no proporciona información sobre el contenido de grasas trans
        
        # Guardamos los rating y reviews de la receta         
        
        interactions = []
        
        collection_interactions = db['food.com_interactions']
        
        for interaction in collection_interactions.find({'recipe_id': row['id']}):
            new_interaction = {
                'user_id': interaction['user_id'],
                'date': interaction['date'],
                'rating': interaction['rating'],
                'review': interaction['review']
            }
            interactions.append(new_interaction)
       
       
        total_rating = 0
        num_interactions = len(interactions)

        for interaction in interactions:
            total_rating += interaction['rating']

        aver_rate = total_rating / num_interactions


        
        nuevo_documento = {
            'title': row['name'],
            'description': row['description'], # Dato solo disponible en Food.com
            'URL': '',
            'foodcom_id': row['id'], # ID de la receta en el dataset
             # Iterate over the interactions and store the desired fields in the 'interactions' field of 'nuevo_documento'
            'source': 'Food.com',
            'language_ISO': 'EN',
            'origin_ISO' : '', # Gastronomía de origen de la receta
            'n_diners': '',
            'category': '',
            'subcategory': '',
            'minutes': row['minutes'],
            'tags': [tag.strip().strip("'") for tag in row['tags'].strip("[]").split(',')], # ['tag1', 'tag2', 'tag3'...]
            'n_ingredients': row['n_ingredients'],
            'ingredients': [ingredient.strip().strip("'") for ingredient in row['ingredients'].strip("[]").split(',')], # ['ingredient1', 'ingredient2', 'ingredient3'...]
            'n_steps': row['n_steps'],
            'steps': [step.strip().strip("'") for step in row['steps'].strip("[]").split(',')], # ['step1', 'step2', 'step3'...]
            'images': [],
            'interactions' : interactions,
            'aver_rate': aver_rate, # Valoración media de la receta
            'num_interactions': num_interactions, # Número de reviews de la receta
            'nutritional_info_100g': {
                'energy': energy,
                'car': car,
                'pro': pro,
                'fat': fat,  
                'sat': sat,
                'trans': '',  
                'salt': salt,
                'sug': sug,
                'fiber': '',
            },
            'nutritional_info_PDV': { # Porcentaje del valor diario de referencia (PDV) por 100 gramos - basado en una dieta de 2000 kcal    
                'energy': energy_PDV,     
                'fat': fat_PDV, 
                'car': car_PDV,
                'pro': pro_PDV,
                'sat': sat_PDV,
                'salt': salt_PDV,
                'sug': sug_PDV,
            },
            'FSA_lights_per100g': {
                'fat': '',
                'salt': '',
                'sat': '',
                'sug': '',
                'energy': '',
                'sod': '',
                'fiber': '',
                'pro': '',
            },
            'OMS_lights_per100g': {
                'fat': oms_lights_fat,
                'trans': '',  # Este dataset no proporciona información sobre el contenido en grasas trans
                'salt': oms_lights_salt,
                'sug': oms_lights_sug,            
            },

        }
        collection.insert_one(nuevo_documento) 
        
        