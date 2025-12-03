import os
from datetime import datetime

def save_history(trip_info):
    """
    Guarda un trayecto en /data/historial.txt
    Compatible con trayectos por tiempo y por distancia.
    """
    os.makedirs('data', exist_ok=True)
    ruta = os.path.join('data', 'historial.txt')
    
    try:
        with open(ruta, 'a', encoding='utf-8') as f:
            f.write("\n==============================\n")
            f.write(f"Fecha: {trip_info['fecha'].strftime('%Y-%m-%d %H:%M:%S')}\n")
            f.write(f"Tipo de trayecto: {trip_info['tipo']}\n")
            
            if trip_info['tipo'] == 'distancia':
                f.write(f"Distancia: {trip_info['distancia_total']} km\n")
                
            if trip_info['tipo'] == 'tiempo':
                f.write(f"Tiempo parado: {trip_info['tiempo_parado']} segundos\n")
                f.write(f"Tiempo en movimiento: {trip_info['tiempo_movimiento']} segundos\n")
                f.write(f"Duración total: {trip_info['duracion_total']} segundos\n")
                
            f.write(f"Coste total: {trip_info['coste_total']} €\n")
            f.write("==============================\n")
    except Exception as e:
        print(f"Error al guardar el historial: {e}")
