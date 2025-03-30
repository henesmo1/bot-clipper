from PyQt6.QtWidgets import QMainWindow

class MainWindow(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(MainWindow, self).__init__(*args, **kwargs)
        self.top_channels = {}  # Inicializar la variable para evitar el error

    def actualizar_ui(self):
        print("Actualizando UI con datos...")