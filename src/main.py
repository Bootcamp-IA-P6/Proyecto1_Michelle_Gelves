import time

def calculate_fare(seconds_stopped, second_moving):
    '''
    funcion para calcular la tarifa total en euros
    stopped: 0.02€/s
    moving: 0.05€/s
    '''
    fare = seconds_stopped * 0.02 + second_moving * 0.05
    print(f'Este es el total de tu viaje: {fare}€')
    return fare

def taximeter():
    '''
    funcion para manejar
    y mostrar las opciones
    del taximetro
    '''
    print('Bienvenido al taximetro')
    print("Comandos disponibles: 'start', 'stop', 'move', 'finish', 'exit' \n")
    trip_activate = False
    start_time = 0
    stopped_time = 0
    moving_time = 0
    state = None
    state_start_time = 0

    while True: 
        command = input('> ').strip().lower()
        if command == 'start':
            if trip_activate:
                print('Error: Hay un viaje en curso')
                continue
            trip_activate = True
            start_time = time.time()
            stopped_time = 0
            moving_time = 0
            state = 'stopped'
            state_start_time = time.time()
            print('El viaje ha sido iniciado. Estado inicial: parado.')

        elif command in ('stop', 'move'):
            if not trip_activate:
                print('Error: No hay un viaje en curso')
                continue
            #Calcula el tiempo del estado anterior
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration
            
            #Cambia el estado
            state = 'stopped' if command == 'stop' else 'moving'
            state_start_time = time.time()
            print(f'El viaje ha sido {command}. Estado actual: {state}.')

        elif command == 'finish':
            if not trip_activate:
                print('Error: No hay un viaje en curso')
                continue
            duration = time.time() - state_start_time
            if state == 'stopped':
                stopped_time += duration
            else:
                moving_time += duration
                
                total_fare = calculate_fare(stopped_time, moving_time)
                print('\n -- Fin del viaje --')
                print(f'Tiempo parado: {stopped_time} segundos')
                print(f'Tiempo en movimiento: {moving_time} segundos')
                print(f'Total a pagar: {total_fare} euros')

                trip_activate = False
                stopped_time = 0
                moving_time = 0
                state = None

        elif command == 'exit':
            print('Saliendo del taximetro, adios!')
            break
        else:
            print('Comando no reconocido. Intenta de nuevo con "start", "stop", "move", "finish". O para salir con "exit".')

if __name__ == '__main__':
    taximeter()
