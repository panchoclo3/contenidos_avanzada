from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, pyqtSignal


class Conejo(QLabel):
    key_pressed = pyqtSignal(int)

    def __init__(self, laberinto, initial_position: list, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap('../assets/sprites/conejo.png').scaled(40, 40))
        self.setGeometry(initial_position[0], initial_position[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.laberinto = laberinto
        self.numero_imagen = 1
        self.orden_imagen = 'arriba'
        self.steps = 5
        self.direction = ''
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.show()

    def colision(self, objeto):
        if self.x() == objeto.x() and self.y() == objeto.y():
            return True
        return False

    def eliminate(self):
        self.hide()
        self.deleteLater()

    def is_valid_position(self, x, y):
        # Calcula la posición de la celda en el laberinto que comienza en (250, 0)
        cell_x = (x - 250) // 40
        cell_y = y // 40

        if 0 <= cell_x < len(self.laberinto[0]) and 0 <= cell_y < len(self.laberinto):
            return self.laberinto[cell_y][cell_x] != 'P'
        return False

    def actualiza_imagen(self):
        if self.numero_imagen == 1:
            if self.orden_imagen == 'arriba':
                self.numero_imagen = 2
            else:
                self.orden_imagen = 'arriba'

        elif self.numero_imagen == 2:
            if self.orden_imagen == 'arriba':
                self.numero_imagen = 3
            else:
                self.numero_imagen = 1

        elif self.numero_imagen == 3:
            if self.orden_imagen == 'arriba':
                self.orden_imagen = 'abajo'
            else:
                self.numero_imagen = 2

    def animate(self, direccion: str):
        if direccion == 'up':
            self.timer.timeout.connect(self.mover_arriba)
        elif direccion == 'down':
            self.timer.timeout.connect(self.mover_abajo)
        elif direccion == 'right':
            self.timer.timeout.connect(self.mover_derecha)
        elif direccion == 'left':
            self.timer.timeout.connect(self.mover_izquierda)
        self.timer.start()

    def mover_arriba(self):
        if self.is_valid_position(self.x(), self.y() - 40):
            self.setPixmap(
                QPixmap(f'../assets/sprites/conejo_arriba_{self.numero_imagen}.png').scaled(40, 40))
            self.setGeometry(self.x(), self.y() - 40, 40, 40)
            self.repaint()
            # self.actualiza_imagen()

        else:
            self.timer.timeout.disconnect(self.mover_arriba)

    def mover_abajo(self):
        if self.is_valid_position(self.x(), self.y() + 40):
            self.setPixmap(
                QPixmap(f'../assets/sprites/conejo_abajo_{self.numero_imagen}.png').scaled(40, 40))
            self.setGeometry(self.x(), self.y() + 40, 40, 40)
            self.repaint()
            # self.actualiza_imagen()

        else:
            self.timer.timeout.disconnect(self.mover_abajo)

    def mover_derecha(self):
        if self.is_valid_position(self.x() + 40, self.y()):
            self.setPixmap(
                QPixmap(f'../assets/sprites/conejo_derecha_{self.numero_imagen}.png').scaled(40, 40))
            self.setGeometry(self.x() + 40, self.y(), 40, 40)
            self.repaint()
            # self.actualiza_imagen()

        else:
            self.timer.timeout.disconnect(self.mover_derecha)

    def mover_izquierda(self):
        if self.is_valid_position(self.x() - 40, self.y()):
            self.setPixmap(
                QPixmap(f'../assets/sprites/conejo_izquierda_{self.numero_imagen}.png').scaled(40, 40))
            self.setGeometry(self.x() - 40, self.y(), 40, 40)
            self.repaint()
            # self.actualiza_imagen()

        else:
            self.timer.timeout.disconnect(self.mover_izquierda)
