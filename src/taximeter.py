import time

def calculate_fare(seconds_stopped, seconds_moving, lang):
    '''
    funcion para calcular la tarifa total en euros
    stopped: 0.02€/s
    moving: 0.05€/s
    '''
    fare = seconds_stopped * 0.02 + seconds_moving * 0.05
    #print(lang["total_fare"].format(fare=fare))
    return fare

def taximeter(lang, commands):
    '''
    funcion para manejar y mostrar las opciones
    del taximetro usando diccionarios de idioma.
    '''
    print(lang["welcome"])
    print(lang["commands"])
    trip_activate = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None
    state_start_time = 0

    while True: 
        command = input('> ').strip().lower()
        
        #Iniciar viaje
        if command == commands["start"]:
            if trip_activate:
                print(lang["start_error"])
                continue
            trip_activate = True
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'
            state_start_time = time.time()
            print(lang["trip_started"])

        #Parar o mover
        elif command in (commands["stop"], commands["move"]):
            if not trip_activate:
                print(lang["no_trip"])
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

        #Finalizar el viaje
        elif command == commands["finish"]:
            if not trip_activate:
                print(lang["no_trip"])
                continue
            
            duration = time.time() - state_start_time
            if state == "stopped":
                stopped_time += duration
            else:
                moving_time += duration
            
            #Calcula la tarifa total
            total_fare = calculate_fare(stopped_time, moving_time, lang)
            
            #Mostrar resumen del viaje
            print(lang["finish_header"])
            print(lang["time_stopped"].format(t=stopped_time))
            print(lang["time_moving"].format(t=moving_time))
            print(lang["total_fare"].format(fare=total_fare))
                

            #Reinicia las variables para un nuevo viaje
            trip_activate = False
            stopped_time = 0
            moving_time = 0
            state = None

        #Salir del programa
        elif command == commands['exit']:
            print(lang["exit"])
            break
        #Comando desconocido
        else:
            print(lang["unknown"])

if __name__ == '__main__':
    taximeter()
