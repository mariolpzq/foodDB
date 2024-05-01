# bd.py

import os
import motor.motor_asyncio

# Inicialización de la conexión a la base de datos
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.tfg

# Definición de las colecciones
bedca_collection = db.get_collection("bedca")
abuela_collection = db.get_collection("abuela")
compounds_collection = db.get_collection("compounds")
ingredientes_collection = db.get_collection("all_ingredients_with_compounds")