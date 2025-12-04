import customtkinter as ctk
from tkinter import messagebox
import time
import os
import logging
from datetime import datetime
from history import save_history
from config import fare_config
from taximeter import calculate_time_fare, calculate_distance_fare, get_distance

# =========================
# Configuración de logging
# =========================
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/taximeter_gui.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

# =========================
# Configuración global
# =========================
config = fare_config()  # Carga tarifas desde .env

# Variables globales para el viaje
trip_active = False
start_time = None
stopped_time = 0
moving_time = 0
state = None

# =========================
# Funciones de control
# =========================

def start_trip():
    '''Inicia un nuevo viaje por tiempo'''
    global trip_active, start_time, stopped_time, moving_time, state
    if trip_active:
        messagebox.showwarning("Advertencia", "Ya hay un viaje en curso")
        logging.error("Intento de iniciar un viaje cuando ya hay uno en curso")
        return
        
    trip_active = True
    start_time = time.time()
    stopped_time = 0
    moving_time = 0
    state = 'stopped'

    messagebox.showinfo("Info", "El viaje ha sido iniciado. Estado inicial: parado.")
    logging.info("Viaje iniciado (modo GUI)")
    
def stop_trip():
    '''cambia el estado a parado para el viaje actual'''
    global trip_active, start_time, stopped_time, moving_time, state
    if not trip_active:
        messagebox.showwarning("Advertencia", "No hay un viaje en curso")
        logging.error("Intento de parar un viaje cuando no hay uno en curso")
        return
    
    now = time.time()
    if state == 'moving':
        moving_time += now - start_time
    else:
        stopped_time += now - start_time
    
    state = 'stopped'
    start_time = now
    update_labels()
    messagebox.showinfo("Info", "El estado ha sido cambiado a parado.")
    logging.info("Estado cambiado a parado")
    
def move_trip():
    '''cambia el estado a en movimiento para el viaje actual'''
    global trip_active, start_time, stopped_time, moving_time, state
    if not trip_active:
        messagebox.showwarning("Advertencia", "No hay un viaje en curso")
        logging.error("Intento de mover un viaje cuando no hay uno en curso")
        return
    
    now = time.time()
    if state == 'stopped':
        stopped_time += now - start_time
    else:
        moving_time += now - start_time
    
    state = 'moving'
    start_time = now
    update_labels()
    messagebox.showinfo("Info", "El estado ha sido cambiado a en movimiento.")
    logging.info("Estado cambiado a en movimiento")
    
def finish_trip():
    '''Finaliza el viaje actual y calcula la tarifa'''
    global trip_active, start_time, stopped_time, moving_time, state
    if not trip_active:
        messagebox.showwarning("Advertencia", "No hay un viaje en curso")
        logging.error("Intento de finalizar un viaje cuando no hay uno en curso")
        return
    
    now = time.time()
    if state == 'stopped':
        stopped_time += now - start_time
    else:
        moving_time += now - start_time
    
    trip_active = False
    total_fare = calculate_time_fare(stopped_time, moving_time)
    messagebox.showinfo(
        "Fin del viaje, resumen: ",
        f"Tiempo parado: {stopped_time:.2f} segundos\n"
        f"Tiempo en movimiento: {moving_time:.2f} segundos\n"
        f"Total a pagar: {total_fare:.2f} euros")
    
    # ===========================
    # GUARDAR EN HISTORIAL
    # ===========================
    trip_info = {
        'fecha': datetime.now(),
        'tipo': 'tiempo',
        'tiempo_parado': round(stopped_time, 2),
        'tiempo_movimiento': round(moving_time, 2),
        'duracion_total': round(stopped_time + moving_time, 2),
        'coste_total': round(total_fare, 2)
    }
    save_history(trip_info)
    logging.info("Trayecto por tiempo guardado en historial")
    
    #reiniciar variables
    reset_time_trip()
    
def start_distance_trip():
    '''Inicia un nuevo viaje por distancia'''
    try:
        distance = float(distance_entry.get())
        if distance <= 0:
            raise ValueError
    except ValueError:
        messagebox.showwarning("Advertencia", "Distancia inválida. Debe ser un número positivo diferente de 0.")
        logging.error("Distancia inválida ingresada para viaje por distancia")
        return
    
    total_fare = calculate_distance_fare(distance)
    
    messagebox.showinfo(
        "Fin del viaje por distancia, resumen: ",
        f"Distancia: {distance:.2f} km\n"
        f"Total a pagar: {total_fare:.2f} euros")
    logging.info(f"Viaje calculado por distancia: {distance} km, Total: {total_fare} €")
    
    #Guardar en historial
    trip_info = {
        'fecha': datetime.now(),
        'tipo': 'distancia',
        'distancia_total': round(distance, 2),
        'coste_total': round(total_fare, 2)
    }
    save_history(trip_info)
    logging.info("Trayecto por distancia guardado en historial: {distance} km, Total: {total_fare} €")
    
def update_distance_fare(event=None):
    '''Actualiza la tarifa mostrada al cambiar la distancia'''
    try:
        distance = float(distance_entry.get())
        if distance <= 0:
            fare_label.config(text="Tarifa actual: 0.00 €")
            return
        fare = calculate_distance_fare(distance)
        fare_distance_label.config(text=f"Tarifa actual: {fare:.2f} €")
    except ValueError:
        fare_distance_label.config(text="Tarifa actual: 0.00 €")
    
def reset_time_trip():
    '''Reinicia las variables para un nuevo viaje por tiempo '''
    global trip_active, start_time, stopped_time, moving_time, state
    trip_active = False
    start_time = None
    stopped_time = 0
    moving_time = 0
    state = None
    update_labels()
    
def update_labels():
    '''Actualiza las etiquetas de la GUI'''
    stopped_label.config(text=f"Tiempo parado: {stopped_time:.2f} s")
    moving_label.config(text=f"Tiempo en movimiento: {moving_time:.2f} s")
    if trip_active:
        fare = calculate_time_fare(stopped_time, moving_time)
        fare_label.config(text=f"Tarifa actual: {fare:.2f} €")
    else:
        fare = 0
        fare_label.config(text="Tarifa actual: 0.00 €")
        
def update_time_labels():
    """Actualiza los tiempos y la tarifa en tiempo real mientras el viaje está activo"""
    global stopped_time, moving_time, start_time
    if trip_active and start_time is not None:
        now = time.time()
        duration = now - start_time
        if state == 'stopped':
            current_stopped = stopped_time + duration
            current_moving = moving_time
        else:
            current_stopped = stopped_time
            current_moving = moving_time + duration
        
        # Actualiza las etiquetas
        stopped_label.config(text=f"Tiempo parado: {current_stopped:.2f} s")
        moving_label.config(text=f"Tiempo en movimiento: {current_moving:.2f} s")
        fare = calculate_time_fare(current_stopped, current_moving)
        fare_label.config(text=f"Tarifa actual: {fare:.2f} €")

    # Vuelve a llamar a esta función después de 1 segundo
    root.after(1000, update_time_labels)


# =========================
# Construcción de la GUI
# =========================
root = tk.Tk()
root.title("Taxímetro GUI")

#Etiqueta de bienvenida
welcome_label = tk.Label(root, text="¡Bienvenido al Taxímetro! Elige una opción para comenzar.", font=("Arial", 15))
welcome_label.pack(pady=10)

#separador
tk.Label(root, text="--- Viaje por Tiempo ---", font=("Arial", 12)).pack(pady=7)

#Labels de información
stopped_label = tk.Label(root, text="Tiempo parado: 0.00 s")
stopped_label.pack()

moving_label = tk.Label(root, text="Tiempo en movimiento: 0.00 s")
moving_label.pack()

fare_label = tk.Label(root, text="Tarifa actual: 0.00 €")
fare_label.pack()

#Botones de control para trayecto por tiempo
frame_buttons = tk.Frame(root)
frame_buttons.pack(pady=5)

start_button = tk.Button(frame_buttons, text="Iniciar", command=start_trip)
start_button.pack(side=tk.LEFT, padx=5)

stop_button = tk.Button(frame_buttons, text="Parar", command=stop_trip)
stop_button.pack(side=tk.LEFT, padx=5)

move_button = tk.Button(frame_buttons, text="Mover", command=move_trip)
move_button.pack(side=tk.LEFT, padx=5)

finish_button = tk.Button(frame_buttons, text="Finalizar", command=finish_trip)
finish_button.pack(side=tk.LEFT, padx=5)

update_time_labels()  # Inicia la actualización automática del tiempo

#separador
tk.Label(root, text="--- Viaje por Distancia ---", font=("Arial", 12)).pack(pady=7)

#Entrada y botón para trayecto por distancia
distance_label = tk.Label(root, text="Introduce la distancia en kilómetros:")
distance_entry = tk.Entry(root)
distance_entry.pack(pady=5)
distance_entry.bind("<KeyRelease>", update_distance_fare)

#Label para tarifa por distancia
fare_distance_label = tk.Label(root, text="Tarifa: -")
fare_distance_label.pack()

#Botón para iniciar viaje por distancia
distance_button = tk.Button(root, text="Calcular Tarifa por Distancia", command=start_distance_trip)
distance_button.pack(pady=5)

#Boton para salir 
exit_button = tk.Button(root, text="Salir", command=root.quit)
exit_button.pack(pady=10)

# Inicia el loop de la GUI
root.mainloop()
