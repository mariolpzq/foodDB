from pymongo import MongoClient
import csv
import pandas as pd
import csv
import json
import ast
import sys

# Aumentar el límite del campo
csv.field_size_limit(100000000)

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['mealrec']

# Nombre del archivo CSV
csv_file = 'mealREC/recipe.csv'


with open(csv_file, 'r', encoding='utf-8-sig') as file:
    reader = csv.DictReader(file)
    for i, row in enumerate(reader):
        #if i % 2 == 0:
            #print(row)

            
            # ----------------------------------------- Información nutricional -----------------------------------------
            
            row['nutritions'] = ast.literal_eval(row['nutritions'])  # Convert to Python dict
            row['nutritions'] = json.dumps(row['nutritions'])  # Convert to JSON string
            row['nutritions'] = json.loads(row['nutritions'])  # Convert JSON string to Python dict      
                            
      
            energy = row['nutritions']['calories']['amount']
            car = row['nutritions']['carbohydrates']['amount']
            pro = row['nutritions']['protein']['amount']
            fat = row['nutritions']['fat']['amount']
            sat = row['nutritions']['saturatedFat']['amount']
            salt = (row['nutritions']['sodium']['amount']/1000) * 2.5
            sug = row['nutritions']['sugars']['amount']
            fiber = row['nutritions']['fiber']['amount']
            
            energy_PDV = round((energy/2000) * 100, 2)
            fat_PDV = round((fat/66) * 100, 2)
            car_PDV = round((car/260) * 100, 2)
            pro_PDV = round((pro/50) * 100, 2)
            sat_PDV = round((sat/22) * 100, 2)
            salt_PDV = round((salt/5) * 100, 2)
            sug_PDV = round((sug/50) * 100, 2)
            
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
                
            # ----------------------------------------- Listado de ingredientes -----------------------------------------
            
            ingredients_list = row['ingredients'].split('^')
            
            # ----------------------------------------- Pasos de la receta -----------------------------------------
            
            row['cooking_directions'] = ast.literal_eval(row['cooking_directions'])  # Convert to Python dict
            row['cooking_directions'] = json.dumps(row['cooking_directions'])
            row['cooking_directions'] = json.loads(row['cooking_directions'])  # Convert JSON string to Python dict

            directions = row['cooking_directions']['directions']
            
            steps = directions.split('\n')
            #steps = [step for step in steps if len(step) >= 9]
                               
            n_steps = len(steps)
            
            # ----------------------------------------- Reviews de la receta -----------------------------------------
            
            row['reviews'] = ast.literal_eval(row['reviews'])  # Convert to Python dict
            row['reviews'] = json.dumps(row['reviews'])
            row['reviews'] = json.loads(row['reviews'])  # Convert JSON string to Python dict
            
            reviews_list = []
            sum_rate = 0
            for user_id, review_data in row['reviews'].items():
                if len(reviews_list) >= 50:
                    break
                user_id = user_id
                rating = review_data['rating']
                date = review_data['dateLastModified']
                review = review_data['text']
                
                review = {
                    'user_id': user_id,
                    'date': date,
                    'rating': rating,
                    'review': review
                }
                
                sum_rate += rating
                
                reviews_list.append(review)
                
            average_rate = sum_rate / len(reviews_list)
            
            num_interactions = len(reviews_list)
                
                
            # ----------------------------------------- Tags de la receta -----------------------------------------
            
            tags = row['tags'].split(';')
            n_tags = len(tags)

            
            # ----------------------------------------- Creación del documento -----------------------------------------

            nuevo_documento = {
                'title': row['recipe_name'],
                'URL': '',
                'source': 'MealREC',
                'language_ISO': 'EN',
                'origin_ISO' : '',
                'n_diners': '',
                'category': '',
                'subcategory': '',
                'minutes': '',
                'n_ingredients': len(ingredients_list),
                'ingredients': ingredients_list,   
                'n_steps': n_steps,
                'steps': steps,
                'images': [],
                'num_interactions': num_interactions, # Número de reviews de la receta
                'interactions': reviews_list,
                'aver_rate': average_rate,
                'num_tags': n_tags,
                'tags' : tags,

                'nutritional_info_100g' : {
                    'energy': energy,
                    'car': car,
                    'pro': pro,
                    'fat': fat,         
                    'sat': sat,
                    'trans': '',  # Necesario calcularlo
                    'salt': salt,
                    'sug': sug,
                    'fiber': fiber,
                },
                'nutritional_info_PDV': { # Porcentaje del valor diario de referencia (PDV) por 100 gramos - basado en una dieta de 2000 kcal
                    'energy': energy_PDV,     
                    'fat': fat_PDV, # 66 gramos de grasas al día
                    'car': car_PDV, # 260 gramos de carbohidratos al día
                    'pro': pro_PDV, # 50 gramos de proteínas al día
                    'sat': sat_PDV, # 22 gramos de grasas saturadas al día
                    'salt': salt_PDV, # 5 gramos de sal al día (2 gramos de sodio)
                    'sug': sug_PDV, # 50 gramos de azúcares al día
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
                    'trans': '',
                    'salt': oms_lights_salt,
                    'sug': oms_lights_sug,           
                },

            }

            collection.insert_one(nuevo_documento)
            print(collection.count_documents({}), "recetas insertadas correctamente")

            
        
    