import pandas as pd
from pymongo import MongoClient

# Cargar el dataset
csv_file = "female.csv"  
data = pd.read_csv(csv_file)


def transformar_fila(fila):
    def convertir_altura_peso(valor):
        try:
            # Si el valor está en el formato 'XXXcm / X' o similar
            if isinstance(valor, str):
                # Eliminar cualquier texto no numérico y convertir a número
                valor_num = ''.join(filter(str.isdigit, valor))
                return int(valor_num) if valor_num else None
            return valor
        except:
            return None


    altura = convertir_altura_peso(fila["Height"])
    peso = convertir_altura_peso(fila["Weight"])



    return {
        "player": {  # Información general 
            "name": fila["Name"],
            "rank": fila["Rank"],
            "age": fila["Age"],
            "position": fila["Position"],
            "team": fila["Team"],
            "nation": fila["Nation"],
            "league": fila["League"],
            "start_year": fila["Start Year"],
        },
        "physical": {  # características físicas
            "height": altura,
            "weight": peso,
        },
        "attributes": {  #atributes 
            "overall": fila["OVR"],
            "speed": { #velocidad
                "acceleration": fila["Acceleration"],
                "sprint_speed": fila["Sprint Speed"],
                "agility": fila["Agility"]
            },
            "shooting": { #disparo
                "finishing": fila["Finishing"],
                "shot_power": fila["Shot Power"],
                "long_shots": fila["Long Shots"],
                "volleys": fila["Volleys"],
                "penalties": fila["Penalties"]
            },
            "passing": { #pases
                "short_passing": fila["Short Passing"],
                "long_passing": fila["Long Passing"],
                "vision": fila["Vision"],
                "crossing": fila["Crossing"],
                "free_kick_accuracy": fila["Free Kick Accuracy"],
                "curve": fila["Curve"]
            },
            "dribbling": { #regate
                "dribbling": fila["Dribbling"],
                "balance": fila["Balance"],
                "ball_control": fila["Ball Control"],
                "composure": fila["Composure"]
            },
            "defending": { #defensa
                "defense": fila["DEF"],
                "interceptions": fila["Interceptions"],
                "heading_accuracy": fila["Heading Accuracy"],
                "defensive_awareness": fila["Def Awareness"],
                "standing_tackle": fila["Standing Tackle"],
                "sliding_tackle": fila["Sliding Tackle"]
            },
            "physicality": { #fisico
                "jumping": fila["Jumping"],
                "stamina": fila["Stamina"],
                "strength": fila["Strength"],
                "aggression": fila["Aggression"]
            },
            "weak_foot": fila["Weak foot"],
            "skill_moves": fila["Skill moves"],
            "preferred_foot": fila["Preferred foot"]
        
        },
        "play_style": fila["play style"].split(", ") if pd.notnull(fila["play style"]) else [],  # Estilo de juego
    }

# Seleccionar solo los primeros 100 registros
data_limited = data.head(100)

# Transformar las primeras 100 filas
data_json = data_limited.apply(transformar_fila, axis=1).tolist()

# Conectar a MongoDB
client = MongoClient("mongodb://root:root@localhost:27017/")  
db = client["jugadoras"]
collection = db["jugadoras_futbol"]

# Insertar los datos
collection.insert_many(data_json)

print("Datos insertados correctamente.")
