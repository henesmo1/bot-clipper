#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
Script de inicio para la aplicación DCS-Clipper

Este script inicia la interfaz gráfica de usuario para DCS-Clipper,
que permite gestionar la creación automática de contenido para redes sociales.
"""

import sys
import os
import logging
from PyQt6.QtWidgets import QApplication
import threading
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QGuiApplication
QGuiApplication.setHighDpiScaleFactorRoundingPolicy(Qt.HighDpiScaleFactorRoundingPolicy.PassThrough)

from src.gui.main_window import MainWindow
from src.core.brain import DCSBrain

import whisper
from scenedetect import open_video, SceneManager, ContentDetector

# Crear la instancia de QApplication
app = QApplication(sys.argv)  # Crear la aplicación después de configurar el DPI

app.setStyle('Fusion')  # Estilo moderno y consistente

# Inicializar el cerebro del sistema
app.brain = DCSBrain()

# Crear y mostrar la ventana principal
window = MainWindow()
window.showMaximized()  # Mostrar en ventana maximizada

# Asegurar que el directorio de logs existe
log_dir = 'logs'
if not os.path.exists(log_dir):
    os.makedirs(log_dir)

# Configurar el sistema de logging
class QtLogHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.setFormatter(logging.Formatter(
            '\033[1;36m%(asctime)s\033[0m - \033[1;32m%(levelname)s\033[0m - \033[1;37m%(name)s\033[0m - \033[1;37m%(message)s\033[0m'
        ))

    def emit(self, record):
        try:
            msg = self.format(record)
            if record.levelno >= logging.ERROR:
                msg = f'\033[1;31m{msg}\033[0m'
            elif record.levelno >= logging.WARNING:
                msg = f'\033[1;33m{msg}\033[0m'
            print(msg, file=sys.stdout, flush=True)
        except Exception as e:
            print(f"Error en el sistema de logging: {e}", file=sys.stderr)

# Configurar el logger principal
root_logger = logging.getLogger()
root_logger.setLevel(logging.DEBUG)

# Eliminar handlers existentes
for handler in root_logger.handlers[:]:
    root_logger.removeHandler(handler)

# Agregar el nuevo handler personalizado
qt_handler = QtLogHandler()
root_logger.addHandler(qt_handler)

# Configurar el logger específico para PyQt
qt_logger = logging.getLogger('PyQt6')
qt_logger.setLevel(logging.DEBUG)

# Redirigir stderr para capturar errores no manejados
sys.stderr = sys.stdout

# Configurar un hook para excepciones no manejadas
def exception_hook(exctype, value, traceback):
    logging.error("Excepción no manejada", exc_info=(exctype, value, traceback))
    sys.__excepthook__(exctype, value, traceback)

sys.excepthook = exception_hook

def main():
    try:
        # Iniciar el bucle de eventos
        sys.exit(app.exec())
    except Exception as e:
        print(f"Error al iniciar la aplicación: {e}")
        logging.error(f"Error al iniciar la aplicación: {e}")
        sys.exit(1)

# Cargar modelo de OpenAI Whisper
model = whisper.load_model("medium")

# Función para transcribir audio
def transcribir_audio(archivo_audio):
    resultado = model.transcribe(archivo_audio)
    return resultado["text"]

# Función para detectar escenas
def detectar_escenas():
    video = open_video("stream.mp4")
    scene_manager = SceneManager()
    scene_manager.add_detector(ContentDetector())
    scene_manager.detect_scenes(frame_source=video)
    scene_list = scene_manager.get_scene_list()
    print("Detección de escenas completada")
    print(scene_list)

def procesar_video():
    print("Procesando video...")

def procesar_video_en_hilo():
    hilo = threading.Thread(target=procesar_video, daemon=True)
    hilo.start()

// threading.Thread(target=detectar_escenas, daemon=True).start();

window.add_button("Iniciar procesamiento", procesar_video_en_hilo);

if __name__ == "__main__":
    app.exec()
# self.setStyleSheet(open("styles.qss", "r").read())  # Comenta esta línea si da error