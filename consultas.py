import json
import time  # Importa el módulo time
from pymongo import MongoClient
from bson import ObjectId  

# Conectar a MongoDB
client = MongoClient("mongodb://root:root@localhost:27017/") 
db = client["jugadoras"]
collection = db["jugadoras_futbol"]

# Función para convertir el ObjectId a string antes de serializar
def json_converter(obj):
    if isinstance(obj, ObjectId):
        return str(obj)  
    return obj

# ----- CONSULTA 1 : Jugadora con año de inicio mayor a 2020 -----
start_time = time.time()  
consulta_1 = collection.find({
    "player.start_year": {"$gt": 2020}  
})

# Guardar resultado en una lista
resultado_1 = []
for jugadora in consulta_1:
    resultado_1.append(jugadora)
end_time = time.time()  
print(f"Timepo consulta 1 (jugadoras iniciaron después de 2020): {end_time - start_time:.4f} segundos")

# ----- CONSULTA 2 : Jugadora cuyo equipo empieza con "Manchester" ----
start_time = time.time()  
consulta_2 = collection.find({
    "player.team": {"$regex": "^Manchester", "$options": "i"}  
})

# Guardar el resultado en una lista
resultado_2 = []
for jugadora in consulta_2:
    resultado_2.append(jugadora)
end_time = time.time()  
print(f"Tiempo consulta 2 (jugadoras cuyo equipo empieza con 'Manchester'): {end_time - start_time:.4f} segundos")

# --- CONSULTA 3 : Jugadora de un país concreto----
pais = "Spain"  
start_time = time.time()  #captura timepo fin
consulta_3 = collection.find({
    "player.nation": pais  
})

# Guardar el resultado en una lista
resultado_3 = []
for jugadora in consulta_3:
    resultado_3.append(jugadora)
end_time = time.time()  #captura timepo fin
print(f"Tiempo consulta 3 (jugadoras de España): {end_time - start_time:.4f} segundos")


 
respuestas = {
    "jugadoras_iniciaron_mayor_2020": resultado_1,
    "jugadoras_manchester": resultado_2,
    "jugadoras_spain": resultado_3
}

# Guardar los resultados 
with open("resultados_jugadoras.json", "w", encoding="utf-8") as f:
    json.dump(respuestas, f, default=json_converter, indent=4)

print("Resultados almacenados en el json")
