# 🧮 Taxímetro Digital 🚕

Proyecto Educativo en el que se desarrolla un prototipo de taxímetro digital utilizando Python. 

## ☑️Demo CLI


## ☑️Demo GUI


## 🎯Objetivos Alcanzados del Proyecto

- Aprender a estructurar un proyecto Python real siguiendo buenas prácticas.
- Separación clara por módulos (config, history, taximeter).
- Gestión de estados (parado / en movimiento).
- Manejo de errores y excepciones personalizadas.
- Logging completo para trazabilidad.
- Inclusión de tests unitarios con pytest.
- Uso de variables de entorno para un sistema configurable.

## 🛠️ Tecnologías Utilizadas

 - Python 3
 - customtkinter 
 - Tkinter 
 - python-dotenv
 - Pytest
 - logging (módulo nativo) 
 - venv 

## 🔗 Control de Versiones

**Git + GitHub Projects** para gestionar la evolución del proyecto:   
- Issues  
- Pull requests 

[Taxímetro Project](https://github.com/users/MichelleGel/projects/2)


## 📁Estructura del proyecto
```bash
taximetro/
│
├── src/
│   ├── taximeter.py        # Lógica principal del taxímetro
│   ├── main.py             # Inicialización del sistema
│   ├── config.py           # Carga de variables de entorno y tarifas
│   ├── history.py          # Lógica del Historial
│   ├── gui.py              # Interfaz Gráfica de Usuario
│   └── tests/
│       └── test_fare.py    # Tests unitarios (pytest)
│   └── languages/
│       └── en.py           # Diccionario para Ingles
│       └── es.py           # Diccionario para Español
│
├── data/
│   └── historial.txt       # Historial persistente de viajes en texto plano (archivo autogenerado)
│
├── logs/
│   └── taximeter.log       # Registro detallado del comportamiento del sistema (archivo autogenerado)
│
├── .env.example           # Configuración editable por el usuario
├── .gitignore             # Ignora /data, /logs y archivos sensibles
├── requirements.txt       # Configuración de dependencias necesarias
└── README.md
```

## 🔑Configuración por Entorno (.env)

Este sistema permite modificar tarifas sin tocar el codigo, mediante variables dentro de un archivo *.env*, estas se cargan mediante una función centralizada en `config.py`

```bash
BASE_FARE=2.0
PRICE_PER_KM=1.25
STOPPED_FARE=0.02
MOVING_FARE=0.05
```

- Crea tu archivo `.env` usando el ejemplo `.env.example` y modifica los valores de las variables a tu gusto.


## 🧩Diagrama de flujo

```text
                  ┌─────────────┐
                  │   Inicio    │
                  └──────┬──────┘
                         │
                         ▼
            Mostrar bienvenida y comandos
                         │
                         ▼
                Esperar comando del usuario
                         │
      ┌─────────────┬─────────────┬─────────────┐
      │             │             │             │
    "start"       "exit"      Desconocido     Otro
      │             │             │             │
      ▼             ▼             ▼             ▼
  Elegir modo    Salir del     Mostrar         Mostrar
  de cálculo     programa      advertencia     advertencia
      │                           
 ┌────┴────┐                     
 │Distancia│                     
 └────┬────┘                     
      │
      ▼
 Solicitar distancia
      │
      ▼
 Validar distancia
      │
      ├──> Distancia inválida ──> Mensaje error → Volver a esperar comando
      │
      ▼
 Calcular tarifa
      │
      ▼
 Mostrar resultado
      │
      ▼
 Guardar historial
      │
      ▼
 Volver a esperar comando
      │
      └─────────────┐
                    │
                Modo tiempo
                    │
                    ▼
             Iniciar viaje
           state = 'stopped'
                    │
                    ▼
          Esperar cambios de estado
        ┌─────┬────────┬───────────┐
        │     │        │           │
      "stop" "move"  "finish"   Otro
        │     │        │           │
        ▼     ▼        ▼           ▼
  state='stopped' state='moving' Calcular tarifa total
        │     │        │           │
        └─────┴────────┴───────────┘
                    │
                    ▼
             Mostrar resumen
           Guardar historial
                    │
                    ▼
           Reiniciar variables
                    │
                    ▼
          Volver a esperar comando
```


## 🧪Testing (pytest)

Los tests implementados se encuentran en `src/tests/test_fare.py`.


#### a) Test de tarifas válidas (_`test_calculate_fare`_)
- Calcula tarifas por tiempo y distancia usando valores correctos.  
- Se asegura de que los resultados sean positivos.

#### b) Test de valores erróneos (_`test_invalid`_)
- Prueba con valores negativos o cero para tiempo y distancia.  
- Se espera que se lance un `ValueError`.

#### c) Test de tarifa conocida (_`test_known_values`_)
- Compara la tarifa calculada con un valor esperado usando la configuración real de tarifas.  
- Garantiza consistencia en el cálculo.

#### d) Test de límites (_`test_fare_limits`_)
- Verifica que el tiempo total 0 produce tarifa 0.  
- Comprueba que valores de distancia cero o negativos generan errores.

#### e) Test de precisión decimal (_`test_decimal_precision`_)
- Asegura que el resultado es un `float` y redondeable a dos decimales.

#### f) Test de valores extremos (_`test_extreme_values`_)
- Valida la correcta operación con valores muy grandes o muy pequeños de distancia.  
- Se asegura que la tarifa sea siempre positiva.

 #### g) Test de tipo inválido (_`test_invalid_type`_)
- Comprueba que se lancen errores cuando se pasan tipos de datos incorrectos (strings en vez de números).


## ▶️Ejecución del proyecto

### 1. Activar el entorno virtual: 
```bash
source venv/bin/activate       # Linux / macOS
source venv/Scripts/activate   # Windows
```

### 2. Instalar las dependencias: 
```bash
pip install -r requirements.txt
```

### 3. Iniciar el programa: 
```bash
python src/main.py
```

### 4. Interfaz Gráfica (GUI):
```bash
python src/gui.py
```

### 5. Ejecutar tests: 
```bash
pytest -v
```

---
##### 👤Desarrollado por Michelle Gelves


