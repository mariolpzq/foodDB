from pymongo import MongoClient
import csv
import pandas as pd
import subprocess

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

# Ejecutar script2.py
#subprocess.run(['python', 'script-bedca.py'])

db = client['tfg']
collection = db['compounds']


# Cargar datos
ingr_info = pd.read_csv('flavor-network/ingr_info.tsv', sep='\t')
if ingr_info is not None:
    print('Datos de los ingredientes cargados correctamente')
else:
    print('Error al cargar los datos de los ingredientes')
    
comp_info = pd.read_csv('flavor-network/comp_info.tsv', sep='\t')
if comp_info is not None:
    print('Datos de los compuestos cargados correctamente')
else:
    print('Error al cargar los datos de los compuestos')
    
ingr_comp = pd.read_csv('flavor-network/ingr_comp.tsv', sep='\t')
if ingr_comp is not None:
    print('Datos de los ingredientes y compuestos cargados correctamente')
else:
    print('Error al cargar los datos de los ingredientes y compuestos')
    

# Crear una colección que relacione los nombres de cada ingrediente con sus compuestos (números CAS)
ingredientes = ingr_info['# id'].tolist()
compuestos = []

for ingrediente in ingredientes:
    compound_ids = ingr_comp.loc[ingr_comp['# ingredient id'] == ingrediente]['compound id']
    cas_numbers = comp_info.loc[comp_info['# id'].isin(compound_ids)]['CAS number']
    cas_numbers = cas_numbers.dropna().tolist() # Eliminar valores nulos
    compuestos.append({'ingredient': str(ingr_info.loc[ingr_info['# id'] == ingrediente]['ingredient name'].values[0]), 'compounds': cas_numbers})

collection.insert_many(compuestos)

print('La colección de ingredientes y compuestos ha sido creada correctamente')

