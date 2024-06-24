# bd.py

import os
import motor.motor_asyncio

# export MONGODB_URL=mongodb://mongoadmin:f00ddb@150.214.203.145:27022/
# export MONGODB_URL=mongodb://mongoadmin:4qJp8wDxA7@localhost:27022/

# Inicialización de la conexión a la base de datos
client = motor.motor_asyncio.AsyncIOMotorClient(os.environ["MONGODB_URL"])
db = client.tfg


def get_collection(collection_name):
    return db.get_collection(collection_name)

# Colecciones de ingredientes
bedca_collection = db.get_collection("bedca")
cofid_collection = db.get_collection("cofid")
ingredientes_collection = db.get_collection("all_ingredients")

# Colecciones de recetas
abuela_collection = db.get_collection("abuela")
recipe1m_collection = db.get_collection("recipe1m")
foodcom_collection = db.get_collection("food.com")
mealrec_collection = db.get_collection("mealrec")
recipeQA_collection = db.get_collection("recipeQA")

# Colecciones de sabores
compounds_collection = db.get_collection("compounds")

# Colecciones de emisiones
emissions_collection = db.get_collection("emissions")

# Colecciones de usuarios
users_collection = db.get_collection("users")

 # Colecciones de dietas
dietas_collection = db.get_collection("diets")