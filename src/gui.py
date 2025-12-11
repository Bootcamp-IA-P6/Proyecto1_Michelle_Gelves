import sys
import os
import time
import logging
from datetime import datetime
from PyQt5.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QTextEdit,
    QVBoxLayout, QHBoxLayout, QMessageBox, QScrollArea
)
from PyQt5.QtGui import QMovie
from PyQt5.QtCore import Qt, QTimer
from history import save_history, read_history 
from config import fare_config
from taximeter import calculate_time_fare, calculate_distance_fare

# =========================
# Logging y configuración
# =========================
if not os.path.exists('logs'):
    os.makedirs('logs')

logging.basicConfig(
    filename='logs/taximeter_gui.log',
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)

config = fare_config()
trip_active = False
start_time = None
stopped_time = 0
moving_time = 0
state = None

# =========================
# Funciones de control
# =========================
def start_trip():
    global trip_active, start_time, stopped_time, moving_time, state
    if trip_active:
        QMessageBox.warning(None, "Advertencia", "Ya hay un viaje en curso")
        logging.error("Intento de iniciar un viaje cuando ya hay uno en curso")
        return
    trip_active = True
    start_time = time.time()
    stopped_time = 0
    moving_time = 0
    state = 'stopped'
    QMessageBox.information(None, "Info", "El viaje ha sido iniciado. Estado inicial: parado.")
    logging.info("Viaje iniciado (modo GUI)")

def stop_trip():
    global trip_active, start_time, stopped_time, moving_time, state
    if not trip_active:
        QMessageBox.warning(None, "Advertencia", "No hay un viaje en curso")
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
    logging.info("Estado de Viaje: parado")

def move_trip():
    global trip_active, start_time, stopped_time, moving_time, state
    if not trip_active:
        QMessageBox.warning(None, "Advertencia", "No hay un viaje en curso")
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
    logging.info("Estado de Viaje: en movimiento")


def finish_trip():
    global trip_active, start_time, stopped_time, moving_time, state
    if not trip_active:
        QMessageBox.warning(None, "Advertencia", "No hay un viaje en curso")
        logging.error("Intento de finalizar un viaje cuando no hay uno en curso")
        return
    now = time.time()
    if state == 'stopped':
        stopped_time += now - start_time
    else:
        moving_time += now - start_time
    trip_active = False
    total_fare = calculate_time_fare(stopped_time, moving_time)
    QMessageBox.information(
        None,
        "Fin del viaje, resumen",
        f"Tiempo parado: {stopped_time:.2f} s\n"
        f"Tiempo en movimiento: {moving_time:.2f} s\n"
        f"Total a pagar: {total_fare:.2f} €"
    )
    #Guardar en Historial
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
    reset_time_trip()

def start_distance_trip():
    try:
        distance = float(gui.distance_entry.text())
        if distance <= 0:
            raise ValueError
    except ValueError:
        QMessageBox.warning(None, "Advertencia", "Distancia inválida. Debe ser un número positivo.")
        logging.error("Distancia inválida ingresada para viaje por distancia")
        return
    total_fare = calculate_distance_fare(distance)
    QMessageBox.information(
        None,
        "Fin del viaje por distancia, resumen: ",
        f"Distancia: {distance:.2f} km\nTotal a pagar: {total_fare:.2f} €"
    )
    trip_info = {
        'fecha': datetime.now(),
        'tipo': 'distancia',
        'distancia_total': round(distance, 2),
        'coste_total': round(total_fare, 2)
    }
    save_history(trip_info)
    logging.info("Trayecto por distancia guardado en historial")
    gui.fare_distance_label.setText("Tarifa actual: 0.00 €")
    gui.distance_entry.clear()

def reset_time_trip():
    global trip_active, start_time, stopped_time, moving_time, state
    trip_active = False
    start_time = None
    stopped_time = 0
    moving_time = 0
    state = None
    
def update_labels():
    gui.stopped_label.setText(f"Tiempo parado: {stopped_time:.2f} s")
    gui.moving_label.setText(f"Tiempo en movimiento: {moving_time:.2f} s")
    if trip_active:
        gui.fare_label.setText(f"Tarifa actual: {calculate_time_fare(stopped_time, moving_time):.2f} €")
    else:
        gui.fare_label.setText("Tarifa actual: 0.00 €")

def update_distance_fare():
    try:
        distance = float(gui.distance_entry.text())
        fare = calculate_distance_fare(distance)
        gui.fare_distance_label.setText(f"Tarifa actual: {fare:.2f} €")
    except ValueError:
        gui.fare_distance_label.setText("Tarifa actual: 0.00 €")

def update_time_labels():
    if trip_active and start_time is not None:
        now = time.time()
        duration = now - start_time
        current_stopped = stopped_time + duration if state == 'stopped' else stopped_time
        current_moving = moving_time + duration if state == 'moving' else moving_time
        gui.stopped_label.setText(f"Tiempo parado: {current_stopped:.2f} s")
        gui.moving_label.setText(f"Tiempo en movimiento: {current_moving:.2f} s")
        gui.fare_label.setText(f"Tarifa actual: {calculate_time_fare(current_stopped, current_moving):.2f} €")

#Mostrar historial
def show_history():
    hist_window = QWidget()
    hist_window.setWindowTitle("Historial de viajes")
    hist_window.setGeometry(150, 150, 500, 500)

    layout = QVBoxLayout()

    title_label = QLabel("Historial de Viajes")
    title_label.setStyleSheet("font-size:16pt; font-weight:bold; color:white;")
    title_label.setAlignment(Qt.AlignCenter)
    layout.addWidget(title_label)

    text_area = QTextEdit()
    text_area.setReadOnly(True)
    text_area.setStyleSheet("background-color:#2B2B2B; color:white; font-family:Consolas; font-size:11pt;")
    text_area.setText(read_history())
    layout.addWidget(text_area)

    hist_window.setLayout(layout)
    hist_window.show()


# =========================
# GUI premium compacta con scroll y fondo animado
# =========================
class TaximeterPremium(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Taxímetro Premium")
        self.setGeometry(100, 100, 600, 650)
        self.setStyleSheet("background-color: rgba(128, 128, 128, 0.75);")

        # --- Fondo GIF ---
        self.bg_label = QLabel(self)
        self.bg_movie = QMovie("src/assets/fondotaxi.gif")
        self.bg_label.setMovie(self.bg_movie)
        self.bg_label.setScaledContents(True)
        self.bg_movie.start()

        # --- Scroll area ---
        self.scroll_area = QScrollArea(self)
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.scroll_area.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.scroll_area.setFrameShape(0)

        self.widgets_container = QWidget()
        self.widgets_container.setAttribute(Qt.WA_TranslucentBackground)
        self.scroll_area.setWidget(self.widgets_container)

        # Construir widgets
        self.init_ui()

        # Timer actualización tiempo
        self.timer = QTimer()
        self.timer.timeout.connect(self.update_time_labels)
        self.timer.start(1000)

    # =========================
    # Ajustar fondo y scroll al redimensionar
    # =========================
    def resizeEvent(self, event):
        super().resizeEvent(event)
        self.bg_label.resize(self.size())
        area_width = min(560, self.width() - 40)
        area_height = min(610, self.height() - 40)
        self.scroll_area.resize(area_width, area_height)
        self.scroll_area.move(
            (self.width() - area_width)//2,
            (self.height() - area_height)//2
        )

    # =========================
    # Construcción de widgets
    # =========================
    def init_ui(self):
        layout = QVBoxLayout()
        layout.setSpacing(10)

        # Bienvenida
        self.welcome_label = QLabel("¡Bienvenido al Taxímetro!\nElige una opción para comenzar.")
        self.welcome_label.setStyleSheet("color:white; font-size:14pt; font-weight:bold; background-color: rgba(0,0,0,0);")
        self.welcome_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(self.welcome_label)

        # Labels tiempo
        self.stopped_label = QLabel("Tiempo parado: 0.00 s")
        self.moving_label = QLabel("Tiempo en movimiento: 0.00 s")
        self.fare_label = QLabel("Tarifa actual: 0.00 €")
        for lbl in [self.stopped_label, self.moving_label, self.fare_label]:
            lbl.setStyleSheet("color:white; background-color: rgba(0,0,0,100); padding:3px; border-radius:6px; font-size:12pt")
            layout.addWidget(lbl)

        # Botones tiempo
        btn_layout = QHBoxLayout()
        self.start_btn = QPushButton("Iniciar"); self.start_btn.clicked.connect(self.start_trip)
        self.stop_btn = QPushButton("Parar"); self.stop_btn.clicked.connect(self.stop_trip)
        self.move_btn = QPushButton("Mover"); self.move_btn.clicked.connect(self.move_trip)
        self.finish_btn = QPushButton("Finalizar"); self.finish_btn.clicked.connect(self.finish_trip)
        for btn, color in zip([self.start_btn, self.stop_btn, self.move_btn, self.finish_btn],
                            ["rgba(76,175,80,200)", "rgba(244,67,54,200)", "rgba(33,150,243,200)", "rgba(255,193,7,200)"]):
            self.setup_button(btn, color); btn_layout.addWidget(btn)
        layout.addLayout(btn_layout)

        # Viaje por distancia
        self.distance_entry = QLineEdit()
        self.distance_entry.setPlaceholderText("Introduce distancia en km")
        self.distance_entry.setStyleSheet("""
            QLineEdit {
                color: white;           /* texto que escribes */
                font-size: 12pt;        /* tamaño del texto */
                background-color: rgba(0,0,0,100); /* fondo semitransparente */
                border-radius: 6px;
                padding: 3px;
            }
            QLineEdit::placeholder {
                color: white;           /* color del placeholder */
                font-size: 14pt;        /* tamaño del placeholder */
            }
        """)
        self.distance_entry.textChanged.connect(self.update_distance_fare)
        self.fare_distance_label = QLabel("Tarifa actual: 0.00 €")
        self.fare_distance_label.setStyleSheet("color:white; background-color: rgba(0,0,0,100); padding:3px; border-radius:6px; font-size:12pt")
        self.distance_btn = QPushButton("Calcular Tarifa por Distancia")
        self.distance_btn.clicked.connect(self.start_distance_trip)
        self.setup_button(self.distance_btn, "rgba(156,39,176,200)")
        for w in [self.distance_entry, self.fare_distance_label, self.distance_btn]:
            layout.addWidget(w)

        # Historial
        self.history_btn = QPushButton("Ver historial")
        self.history_btn.clicked.connect(self.show_history)
        self.setup_button(self.history_btn, "rgba(121,85,72,200)")
        layout.addWidget(self.history_btn)

        # Salir
        self.exit_btn = QPushButton("Salir")
        self.exit_btn.clicked.connect(self.close)
        self.setup_button(self.exit_btn, "rgba(96,125,139,200)")
        layout.addWidget(self.exit_btn)

        self.widgets_container.setLayout(layout)

    # =========================
    # Estilo botones
    # =========================
    def setup_button(self, button, color):
        button.setStyleSheet(f"""
            QPushButton {{
                background-color: {color};
                color:white;
                padding:5px;
                border-radius:6px;
                font-weight:bold;
            }}
            QPushButton:hover {{
                background-color: rgba(255,255,255,50);
            }}
        """)

    # =========================
    # Funciones actualización labels
    # =========================
    def update_time_labels(self):
        global start_time, stopped_time, moving_time, state
        if trip_active and start_time is not None:
            now = time.time()
            duration = now - start_time
            current_stopped = stopped_time + duration if state == 'stopped' else stopped_time
            current_moving = moving_time + duration if state == 'moving' else moving_time
            self.stopped_label.setText(f"Tiempo parado: {current_stopped:.2f} s")
            self.moving_label.setText(f"Tiempo en movimiento: {current_moving:.2f} s")
            self.fare_label.setText(f"Tarifa actual: {calculate_time_fare(current_stopped, current_moving):.2f} €")

    def update_distance_fare(self):
        try:
            distance = float(self.distance_entry.text())
            fare = calculate_distance_fare(distance)
            self.fare_distance_label.setText(f"Tarifa actual: {fare:.2f} €")
        except ValueError:
            self.fare_distance_label.setText("Tarifa actual: 0.00 €")

    # =========================
    # Funciones control del viaje
    # =========================
    def start_trip(self):
        global trip_active, start_time, stopped_time, moving_time, state
        if trip_active:
            return
        trip_active = True
        start_time = time.time()
        stopped_time = 0
        moving_time = 0
        state = 'stopped'

    def stop_trip(self):
        global start_time, stopped_time, moving_time, state
        if not trip_active:
            return
        now = time.time()
        if state == 'moving':
            moving_time += now - start_time
        else:
            stopped_time += now - start_time
        state = 'stopped'
        start_time = now

    def move_trip(self):
        global start_time, stopped_time, moving_time, state
        if not trip_active:
            return
        now = time.time()
        if state == 'stopped':
            stopped_time += now - start_time
        else:
            moving_time += now - start_time
        state = 'moving'
        start_time = now

    def finish_trip(self):
        global trip_active, start_time, stopped_time, moving_time, state
        if not trip_active:
            return
        now = time.time()
        if state == 'stopped':
            stopped_time += now - start_time
        else:
            moving_time += now - start_time
        trip_active = False
        start_time = None
        state = None

    def start_distance_trip(self):
        try:
            distance = float(self.distance_entry.text())
            if distance <= 0:
                return
            fare = calculate_distance_fare(distance)
            self.fare_distance_label.setText(f"Tarifa actual: {fare:.2f} €")
        except ValueError:
            self.fare_distance_label.setText("Tarifa actual: 0.00 €")

    # =========================
    # Historial
    # =========================
    def show_history(self):
        self.hist_window = QWidget()
        self.hist_window.setWindowTitle("Historial de viajes")
        self.hist_window.setGeometry(150, 150, 500, 500)

        layout = QVBoxLayout()
        text_area = QTextEdit()
        text_area.setReadOnly(True)
        text_area.setText(read_history())
        text_area.setStyleSheet("background-color:#2B2B2B; color:white; font-family:Consolas; font-size:11pt;")
        layout.addWidget(text_area)

        self.hist_window.setLayout(layout)
        self.hist_window.show()

# =========================
# Ejecutar app
# =========================
app = QApplication(sys.argv)
gui = TaximeterPremium()
gui.show()
sys.exit(app.exec_())