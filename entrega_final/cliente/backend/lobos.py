from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer


class LoboV(QLabel):
    def __init__(self, laberinto, initial_position: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/lobo_vertical_arriba_1.png').scaled(40, 40))
        self.setGeometry(initial_position[0], initial_position[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.laberinto = laberinto
        self.arriba = True
        self.numero_imagen = 1
        self.orden_imagen = 'arriba'
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.animate)
        self.timer.start(500)
        self.show()

    def stop(self):
        self.timer.stop()

    def eliminate(self):
        self.hide()

    def animate(self):
        if self.arriba:
            self.mover_arriba()
        else:
            self.mover_abajo()

    def mover_arriba(self):
        if self.is_valid_position(self.x(), self.y() - 40):
            self.setPixmap(
                QPixmap(f'../assets/sprites/lobo_vertical_arriba_{self.numero_imagen}.png').scaled(40, 40))
            self.setGeometry(self.x(), self.y() - 40, 40, 40)
            self.repaint()
            self.actualiza_imagen()
            self.raise_()
        else:
            self.arriba = False

    def mover_abajo(self):
        if self.is_valid_position(self.x(), self.y() + 40):
            self.setPixmap(
                QPixmap('../assets/sprites/lobo_vertical_abajo_1.png').scaled(40, 40))
            self.setGeometry(self.x(), self.y() + 40, 40, 40)
            self.repaint()
            self.actualiza_imagen()
            self.raise_()
        else:
            self.arriba = True

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


class LoboH(QLabel):
    def __init__(self, laberinto, initial_position: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/lobo_horizontal_derecha_1.png').scaled(40, 40))
        self.setGeometry(initial_position[0], initial_position[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.laberinto = laberinto
        self.derecha = True
        self.timer = QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.animate)
        self.timer.start(500)
        self.show()

    def stop(self):
        self.timer.stop()

    def eliminate(self):
        self.hide()
        self.deleteLater()

    def animate(self):
        if self.derecha:
            self.mover_derecha()
        else:
            self.mover_izquierda()

    def mover_derecha(self):
        if self.is_valid_position(self.x() + 40, self.y()):
            self.setPixmap(
                QPixmap('../assets/sprites/lobo_horizontal_derecha_1.png').scaled(40, 40))
            self.setGeometry(self.x() + 40, self.y(), 40, 40)
            self.repaint()
            self.raise_()
        else:
            self.derecha = False

    def mover_izquierda(self):
        if self.is_valid_position(self.x() - 40, self.y()):
            self.setPixmap(
                QPixmap('../assets/sprites/lobo_horizontal_izquierda_1.png').scaled(40, 40))
            self.setGeometry(self.x() - 40, self.y(), 40, 40)
            self.repaint()
            self.raise_()
        else:
            self.derecha = True

    def is_valid_position(self, x, y):
        # Calcula la posición de la celda en el laberinto que comienza en (250, 0)
        cell_x = (x - 250) // 40
        cell_y = y // 40

        if 0 <= cell_x < len(self.laberinto[0]) and 0 <= cell_y < len(self.laberinto):
            return self.laberinto[cell_y][cell_x] != 'P'
        return False
