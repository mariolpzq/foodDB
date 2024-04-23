    
import pymongo
import json
from pymongo import MongoClient
import csv
import pandas as pd

MONGO_URI = 'mongodb://localhost:27022/'

client = MongoClient(MONGO_URI, username='mongoadmin', password='4qJp8wDxA7')

db = client['tfg']
collection = db['recipe1m_originals']

# Cargar datos desde el archivo JSON
with open('recipe1M/layer1.json', 'r') as archivo_json_original:
    datos_originales = json.load(archivo_json_original)

collection.insert_many(datos_originales)
print("Datos originales de Recipe1M insertados correctamente")
