from PyQt6.QtWidgets import QWidget
from PyQt6.QtCore import pyqtSignal
from frontend.clases_graficas import Imagen, Etiqueta, Caja, Boton, Tablero


class VentanaInicio(QWidget):

    signal_tablero = pyqtSignal(list)
    signal_usuario = pyqtSignal(str)
    signal_cerrar = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.lista_tablero = []
        self.inicializa_gui()

    def inicializa_gui(self):
        self.setGeometry(400, 200, 500, 500)
        self.setWindowTitle('DCConejoChico')
        self.setStyleSheet('background-color: pink')

        self.logo = Imagen('../assets/sprites/logo.png',
                           (80, 10), (340, 100), self)

        self.sub_titulo = Etiqueta(
            '¿Una partida?', 20, (170, 120), self)

        self.caja = Caja((100, 150), self)
        self.caja.setPlaceholderText('Ingrese nombre de usuario')

        self.boton_ingresar = Boton('Ingresar', (100, 200), self)
        self.boton_ingresar.clicked.connect(self.on_ingresar_clicked)
        self.boton_close = Boton('Salir', (300, 200), self)
        self.boton_close.clicked.connect(self.close)

        self.tablero = Tablero((50, 250), self)

        self.show()

    def display_tablero(self, tablero: list):
        self.tablero.display(tablero[0], tablero[1])

    def on_ingresar_clicked(self):
        usuario = self.caja.text()
        self.signal_usuario.emit(usuario)

    def usuario_invalido(self):
        self.caja.clear()
        self.caja.setPlaceholderText('Usuario inválido')

    def usuario_blockeado(self):
        self.caja.clear()
        self.caja.setPlaceholderText('Usuario bloqueado')

    def closeEvent(self, event):
        self.signal_cerrar.emit()
        event.accept()
