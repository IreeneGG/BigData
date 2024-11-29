from pymongo import MongoClient

# Conectar a MongoDB
client = MongoClient("mongodb://root:root@localhost:27017/")  
db = client["jugadoras"]
collection = db["jugadoras_futbol"]


jugadoras = [
    {"name": "Aitana Bonmatí"},
    {"name": "Alexia Putellas"},
]

# Modificar el nombre de las jugadoras a mayúsculas
for jugadora in jugadoras:
    collection.update_one(
        {"player.name": jugadora["name"]},  
        {"$set": {"player.name": jugadora["name"].upper()}}  
    )

print("Los nombres de las jugadoras han sido actualizados.")
