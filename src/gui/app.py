import os
import sys
import logging
from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel
from PyQt6.QtCore import Qt

class AppStatusWidget(QWidget):
    """Widget para mostrar el estado del sistema."""
    
    def __init__(self, app=None):
        super().__init__()
        self.app = app
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout(self)
        
        # Etiqueta de estado
        self.status_label = QLabel("Estado del sistema: Operacional")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.addWidget(self.status_label)
        
        # Actualizar estado
        self.update_status()
        
    def update_status(self):
        """Actualiza la información de estado del sistema."""
        try:
            if hasattr(self.app, 'brain') and hasattr(self.app.brain, 'get_system_status'):
                status = self.app.brain.get_system_status()
                self.status_label.setText(f"Estado del sistema: {status['system_health']}")
            else:
                self.status_label.setText("Estado del sistema: No disponible")
        except Exception as e:
            logging.error(f"Error al obtener estado del sistema: {e}")
            self.status_label.setText("Estado del sistema: Error")