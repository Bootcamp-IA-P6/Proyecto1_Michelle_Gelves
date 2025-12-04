import os
from dotenv import load_dotenv

def fare_config():
    '''
    Carga tarifas desde .env.
    Si no existe crea uno con valores por defecto.
    Valida que los valores sean numéricos.
    '''
    
    #Crear archivo por defecto si no existe
    if not os.path.exists('.env'):
        with open('.env', 'w') as f:
            f.write('BASE_FARE=1.5\n')
            f.write('PRICE_PER_KM=0.25\n')
            f.write('STOPPED_FARE=0.02\n')
            f.write('MOVING_FARE=0.05\n')

    #cargar variables del .env
    load_dotenv()
    
    def get_float(key, default):
        """Convierte la variable a float. Si falla, devuelve por defecto."""
        try:
            return float(os.getenv(key, default))
        except (ValueError, TypeError):
            print(f"Advertencia: {key} no es numérico en .env. Se usará el valor por defecto: ({default}).")
            return default
        
    config = {
        'base_fare': get_float('BASE_FARE', 1.5),
        'price_per_km': get_float('PRICE_PER_KM', 0.25),
        'stopped_fare': get_float('STOPPED_FARE', 0.02),
        'moving_fare': get_float('MOVING_FARE', 0.05),
    }
    
    return config

if __name__ == '__main__':
    fare_config()