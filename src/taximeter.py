import time
import os
import logging
from history import save_history
from datetime import datetime

# =========================
# Configuración de logging
# =========================
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/taximeter.log', 
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =========================
# Función de tarifa
# =========================

def calculate_time_fare(seconds_stopped, seconds_moving):
    '''
    funcion para calcular la tarifa usando tiempo.
    stopped: 0.02€/s
    moving: 0.05€/s
    '''
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    #print(lang["total_fare"].format(fare=fare))
    return fare

def calculate_distance_fare(distance):
    '''
    funcion para calcular la tarifa usando distancia.
    '''
    base_fare = 1.5       #Euros fijos al inciar el viaje
    price_per_km = 0.25   #Euros por km
    fare = base_fare + distance * price_per_km
    #print(lang["total_fare"].format(fare=fare))
    return fare

#Función validador de distancia
def get_distance(lang):
    '''
    Pide al ususario la distancia y maneja errores de entrada.
    '''
    while True:
        try:
            distance = float(input(lang["enter_distance"]))
            if distance <= 0:
                print(lang["invalid_distance"])
                logging.error(f"Distancia introducida por el usuario no válida: {distance} km")
                continue
            return distance
        except ValueError:
            print(lang["invalid_distance"])

# =========================
# Función principal
# =========================
def taximeter(lang, commands):
    '''
    funcion para manejar y mostrar las opciones
    del taximetro usando diccionarios de idioma.
    '''
    trip_activate = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None
    state_start_time = 0
    
    print(lang["welcome"])
    print(lang["commands"])

    while True: 
        command = input('> ').strip().lower()
        
        #Iniciar viaje
        if command == commands["start"]:
            if trip_activate:
                print(lang["start_error"])
                logging.error("Intento de inicio de viaje cuando ya hay un viaje en curso")
                continue
            
            trip_activate = True
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'
            state_start_time = time.time()
            
            # Elegir modo de cálculo
            mode = input(lang["choose_mode"]).strip().lower()
            if mode in ("distancia", "distance"):
                try:
                    distance = get_distance(lang)
                    total_fare = calculate_distance_fare(distance)
                    print(lang["total_fare"].format(fare=total_fare))
                    logging.info(f"Viaje calculado por distancia: {distance} km, Total: {total_fare} €")
                
                    trip_info = {
                        "fecha": datetime.now(),
                        "tipo": "distancia",
                        "distancia_total": round(distance, 2),
                        "coste_total": round(total_fare, 2)
                    }
                    save_history(trip_info)
                    logging.info("Trayecto por distancia guardado en historial")
                
                except ValueError:
                    print(lang["invalid_distance"])
                    logging.error("Distancia inválida introducida por el usuario")
                    
                # Reiniciar variables para permitir nuevo viaje
                trip_activate = False
                continue
            
            print(lang["trip_started"])
            logging.info("Viaje iniciado (modo tiempo)")

        #Cambio de estado
        elif command in (commands["stop"], commands["move"]):
            if not trip_activate:
                print(lang["no_trip"])
                logging.error("Intento de cambio de estado sin viaje en curso")
                continue
            
            #Calcula el tiempo del estado anterior
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration
            
            #Cambia el estado
            state = 'stopped' if command == commands["stop"] else 'moving'
            state_start_time = time.time()
            
            #Muestra el cambio de estado usando el diccionario
            if state == 'stopped':
                print(lang["state_changed"].format(cmd=lang["cmd_stop"], state=lang["cmd_stop"]))
            else:
                print(lang["state_changed"].format(cmd=lang["cmd_move"], state=lang["cmd_move"]))
            logging.info(f"Cambio de estado a {state}")

        #Finalizar el viaje
        elif command == commands["finish"]:
            if not trip_activate:
                print(lang["no_trip"])
                logging.error("Intento de finalizar viaje sin viaje activo")
                continue
            
            duration = time.time() - state_start_time
            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration
            
            #Mostrar resumen del viaje
            print(lang["finish_header"])
            print(lang["time_stopped"].format(t=stopped_time))
            print(lang["time_moving"].format(t=moving_time))
            
            #Calcula la tarifa total
            total_fare = calculate_time_fare(stopped_time, moving_time)
            print(lang["total_fare"].format(fare=total_fare))
            logging.info(f"Viaje finalizado. Total: {total_fare:.2f} €")    

            # ===========================
            # CREAR TRAYECTO PARA HISTORIAL
            # ===========================
            trip_info = {
                "fecha": datetime.now(),
                "tipo": "tiempo",
                "tiempo_parado": round(stopped_time, 2),
                "tiempo_movimiento": round(moving_time, 2),
                "duracion_total": round(stopped_time + moving_time, 2),
                "coste_total": round(total_fare, 2)
            }

            save_history(trip_info)
            logging.info("Trayecto por tiempo guardado en historial")

            #Reinicia las variables para un nuevo viaje
            trip_activate = False
            stopped_time = 0
            moving_time = 0
            state = None

        #Salir del programa
        elif command == commands['exit']:
            print(lang["exit"])
            logging.info("Usuario ha salido del programa")
            break
        #Comando desconocido
        else:
            print(lang["unknown"])
            logging.warning(f"Comando desconocido introducido: {command}")

if __name__ == '__main__':
    taximeter()
