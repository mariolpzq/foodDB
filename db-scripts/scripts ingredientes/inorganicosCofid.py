from pymongo import MongoClient
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['cofid']

# Nombre del archivo Excel
excel_file = 'hojaSalCoFID.xlsx'

# Lee el archivo Excel
df = pd.read_excel(excel_file)

# Procesa cada fila del DataFrame
for index, row in df.iterrows():
    name_en = row['Food Name']

    if row['Sodium (mg)'] == 'Tr' or row['Sodium (mg)'] == 'N':
        sodio = 0
        sal = ''
    else: 
        sodio = float(row['Sodium (mg)'])
        sal = sodio * 2.5 / 1000

    if row['Potassium (mg)'] == 'Tr' or row['Potassium (mg)'] == 'N':
        potasio = 0
    else:
        potasio = float(row['Potassium (mg)'])

    if row['Calcium (mg)'] == 'Tr' or row['Calcium (mg)'] == 'N':
        calcio = 0
    else:
        calcio = float(row['Calcium (mg)'])
        
    if row['Magnesium (mg)'] == 'Tr' or row['Magnesium (mg)'] == 'N':
        magnesio = 0
    else:
        magnesio = float(row['Magnesium (mg)'])

    if row['Phosphorus (mg)'] == 'Tr' or row['Phosphorus (mg)'] == 'N':
        fosforo = 0
    else:
        fosforo = float(row['Phosphorus (mg)'])

    if row['Iron (mg)'] == 'Tr' or row['Iron (mg)'] == 'N':
        hierro = 0
    else:
        hierro = float(row['Iron (mg)'])

    if row['Chloride (mg)'] == 'Tr' or row['Chloride (mg)'] == 'N':
        cloruro = 0
    else:
        cloruro = float(row['Chloride (mg)'])

    oms_lights_salt = ""   

    if sal != '':
        if sal <= 0.3 :
            oms_lights_salt = "green"
        elif 0.3 < sal <= 1.5 :
            oms_lights_salt = "orange"
        else:
            oms_lights_salt = "red"

    # Actualiza los ingredientes de la base de datos
    collection.update_one(
        {'name_en': name_en}, 
        {
            '$set': {
                'nutritional_info_100g.sod': sodio, 
                'nutritional_info_100g.pot': potasio, 
                'nutritional_info_100g.cal': calcio, 
                'nutritional_info_100g.mag': magnesio, 
                'nutritional_info_100g.phos': fosforo, 
                'nutritional_info_100g.iron': hierro, 
                'nutritional_info_100g.chloride': cloruro, 
                'nutritional_info_100g.salt': sal, 
                'oms_lights.salt': oms_lights_salt
            }
        }
    )

print("Todas las filas han sido procesadas y actualizadas en la base de datos.")
