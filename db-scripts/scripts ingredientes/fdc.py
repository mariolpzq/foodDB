import csv
from pymongo import MongoClient
from collections import OrderedDict # Para mantener el orden de los campos en los documentos de alimentos

# Conexión a la base de datos
MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']


#---------- Leer los CSV ------------------------------------------------------------------------------------------------------------------------------------------------------


# Función para cargar datos de un archivo CSV a un diccionario
def cargar_datos_csv(archivo):
    datos = []
    with open(archivo, 'r', encoding='utf-8-sig') as csvfile:
        reader = csv.DictReader(csvfile, delimiter=';')
        for row in reader:
            datos.append(dict(row))
    return datos

# Cargar datos de los archivos CSV
alimentos = cargar_datos_csv('fdc/food.csv')
if alimentos is None or alimentos is []:
    print('Error al cargar los datos de alimentos')
#else:
    #print(alimentos)
    
categorias_alimentos = cargar_datos_csv('fdc/food_category.csv')
if categorias_alimentos is None:
    print('Error al cargar los datos de categorías de alimentos')
    
nutrientes = cargar_datos_csv('fdc/nutrient.csv')
if nutrientes is None:
    print('Error al cargar los datos de nutrientes')
    
alimentos_nutrientes = cargar_datos_csv('fdc/food_nutrient.csv')
if alimentos_nutrientes is None:
    print('Error al cargar los datos de nutrientes de alimentos')
#else:
    #print(alimentos_nutrientes)
    
    
#---------- Importar los datos ------------------------------------------------------------------------------------------------------------------------------------------------------


# Construir un diccionario que mapee los IDs de alimentos a sus respectivos documentos
alimentos_dict = {alimento['fdc_id']: alimento for alimento in alimentos}

# Añadir información de la categoría de alimentos a cada alimento
for alimento in alimentos_dict.values():
    categoria = next((c for c in categorias_alimentos if c['id'] == alimento['food_category_id']), None)
    if categoria:
        alimento['category_esp'] = categoria['category_esp']
        alimento['category_en'] = categoria['category_en']
    del alimento['food_category_id']  # Eliminar el ID de categoría ahora que ya tenemos la información

# Añadir información de los nutrientes a cada alimento
for alimento_nutriente in alimentos_nutrientes:
    alimento_id = alimento_nutriente['fdc_id']
    nutriente_id = alimento_nutriente['nutrient_id']
    cantidad = alimento_nutriente['amount']

    if alimento_id in alimentos_dict:
        nutriente_nombre = next((n['name'] for n in nutrientes if n['id'] == nutriente_id), None)
        if nutriente_nombre:
            if 'nutritional_info_100g' not in alimentos_dict[alimento_id]:
                alimentos_dict[alimento_id]['nutritional_info_100g'] = { 'fats': {} }
            
            if nutriente_nombre == 'total_fat':
                alimentos_dict[alimento_id]['nutritional_info_100g']['fats']['total_fat'] = float(cantidad)
            elif nutriente_nombre == 'sat':
                alimentos_dict[alimento_id]['nutritional_info_100g']['fats']['sat'] = float(cantidad)
            elif nutriente_nombre == 'trans':
                alimentos_dict[alimento_id]['nutritional_info_100g']['fats']['trans'] = float(cantidad)
            else: 
                alimentos_dict[alimento_id]['nutritional_info_100g'][nutriente_nombre] = float(cantidad)


#---------- Añadir campos faltantes a los documentos de alimentos ------------------------------------------------------------------------------------------------------------------------------------------------------
 
 
# Definir el esquema de los alimentos
alimento_esquema = {
    'name_esp': "",
    'name_en': "",
    'langual': "",
    'origin_ISO': 'USA',
    'source': 'FDC',    
    'category_esp': "",
    'category_en': "", 
    'edible': "",            
    'compounds': [],
    'nutritional_info_100g': {
        'car':"",
        'energy_kcal': "",
        'energy_kj': "",
        'pro': "",
        'wat': "",
        'sug': "",
        "fats": {
            "total_fat": "",
            "sat": "",
            "trans": "",
        },
        'fiber': "",
        'cal': "",
        'chloride': "",
        'iron': "",
        'pot': "",
        'mag': "",
        'sod': "",
        'salt': "",
        'phos': "",
        'cholesterol': "",
    },
    'oms_lights': {
        'salt': "",
        'sug': "",
        'total_fat': "",
        'trans': "",
    },
}

# Definimos un diccionario que mantiene el orden en el que insertamos los datos y recorremos el esquema de los alimentos, añadiendo los campos faltantes a cada documento de alimentos en el orden correcto

for alimento in alimentos_dict.values():
    ordered_alimento = OrderedDict()
    for field in alimento_esquema:
        if field in alimento:
            ordered_alimento[field] = alimento[field]
        else:
            ordered_alimento[field] = alimento_esquema[field]
    alimento.clear()
    # Actualizar el documento de alimento con los campos faltantes en el orden correcto
    alimento.update(ordered_alimento)
    
    # Añadir campos faltantes a los documentos de nutrientes
    if 'nutritional_info_100g' in alimento:
        nutritional_info = alimento['nutritional_info_100g']
        ordered_nutritional_info = OrderedDict()
        for nutrient in alimento_esquema['nutritional_info_100g']:
            if nutrient in nutritional_info:
                ordered_nutritional_info[nutrient] = nutritional_info[nutrient]
            else:
                ordered_nutritional_info[nutrient] = alimento_esquema['nutritional_info_100g'][nutrient]
        alimento['nutritional_info_100g'] = ordered_nutritional_info
                
    # Añadir campos faltantes a los documentos de grasas
    if 'fats' in alimento['nutritional_info_100g']:
        fats = alimento['nutritional_info_100g']['fats']
        ordered_fats = OrderedDict()
        for type_of_fat in alimento_esquema['nutritional_info_100g']['fats']:
            if type_of_fat in fats:
                ordered_fats[type_of_fat] = fats[type_of_fat]
            else:
                ordered_fats[type_of_fat] = alimento_esquema['nutritional_info_100g']['fats'][type_of_fat]
        alimento['nutritional_info_100g']['fats'] = ordered_fats
        
        
#---------- Añadir valor de "salt" y de los semáforos nutricionales ------------------------------------------------------------------------------------------------------------------------------------------------------


for alimento in alimentos_dict.values():
    oms_lights_salt, oms_lights_sug, oms_lights_total_fat, omg_lights = "", "", "", ""
    
    if 'nutritional_info_100g' in alimento:
        nutritional_info = alimento['nutritional_info_100g']
        
        if 'sod' in nutritional_info and nutritional_info['sod'] != '':
            alimento['nutritional_info_100g']['salt'] = float(nutritional_info['sod']) * 2.5
        else:
            alimento['nutritional_info_100g']['salt'] = ""
        
        
        
        if 'salt' in nutritional_info and nutritional_info['salt'] != '':  
                salt = float(nutritional_info['salt'])   
                         
                if salt <= 0.3 :
                    oms_lights_salt = "green"
                elif 0.3 < salt <= 1.5 :
                    oms_lights_salt = "orange"
                else:
                    oms_lights_salt = "red"
                    
        if 'sug' in nutritional_info and nutritional_info['sug'] != '':
            sug = float(nutritional_info['sug'])
                
            if sug <= 5 :
                oms_lights_sug = "green"
            elif 5 < sug <= 22.5 :
                oms_lights_sug = "orange"
            else:
                oms_lights_sug = "red"
                
        if 'total_fat' in nutritional_info['fats'] and nutritional_info['fats']['total_fat'] != '':
            total_fat = float(nutritional_info['fats']['total_fat'])
            
            if total_fat <= 3 :
                oms_lights_total_fat = "green"
            elif 3 < total_fat <= 17.5 :
                oms_lights_total_fat = "orange"
            else:
                oms_lights_total_fat = "red"
                
        if 'trans' in nutritional_info['fats'] and nutritional_info['fats']['trans'] != '':
            trans = float(nutritional_info['fats']['trans'])
            
            if trans <= 0.5 :
                omg_lights_trans = "green"
            elif 0.5 < trans <= 2.0 :
                omg_lights_trans = "orange"
            else:
                omg_lights_trans = "red"
                    
    alimento['oms_lights'] = {
        'salt': oms_lights_salt,
        'sug': oms_lights_sug,
        'total_fat': oms_lights_total_fat,
        'trans': omg_lights_trans,
    }
            
      
#---------- # Insertar documentos en la colección ------------------------------------------------------------------------------------------------------------------------------------------------------

fdc = list(alimentos_dict.values())
db.fdc.insert_many(fdc)

print("Datos insertados correctamente en la colección 'fdc' de la base de datos MongoDB.")
