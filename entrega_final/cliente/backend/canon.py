from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, pyqtSignal


class CanonRight(QLabel):
    carrot_signal = pyqtSignal()

    def __init__(self, posicion: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/canon_derecha.png').scaled(40, 40))
        self.posicion = posicion
        self.setGeometry(self.posicion[0], self.posicion[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()


class CanonLeft(QLabel):
    def __init__(self, posicion: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/canon_izquierda.png').scaled(40, 40))
        self.posicion = posicion
        self.setGeometry(self.posicion[0], self.posicion[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()


class CanonUp(QLabel):

    def __init__(self, posicion: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/canon_arriba.png').scaled(40, 40))
        self.posicion = posicion
        self.setGeometry(self.posicion[0], self.posicion[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()


class CanonDown(QLabel):
    def __init__(self, posicion: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/canon_abajo.png').scaled(40, 40))
        self.posicion = posicion
        self.setGeometry(self.posicion[0], self.posicion[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()


class Carrot(QLabel):

    def __init__(self, laberinto, type: str, initial_position: list, parent=None):
        super().__init__(parent)
        self.lista_zanahorias = ['../assets/sprites/zanahoria_arriba.png', '../assets/sprites/zanahoria_abajo.png',
                                 '../assets/sprites/zanahoria_derecha.png', '../assets/sprites/zanahoria_izquierda.png']
        self.tipo = type
        if self.tipo == 'arriba':
            self.image = self.lista_zanahorias[0]
        elif self.tipo == 'abajo':
            self.image = self.lista_zanahorias[1]
        elif self.tipo == 'derecha':
            self.image = self.lista_zanahorias[2]
        elif self.tipo == 'izquierda':
            self.image = self.lista_zanahorias[3]
        self.initial_position = initial_position
        self.setPixmap(
            QPixmap(self.image).scaled(40, 40))
        self.setGeometry(initial_position[0], initial_position[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.laberinto = laberinto
        self.timer = QTimer(self)
        self.timer.setInterval(200)
        self.timer.timeout.connect(self.animate)
        self.timer.start(200)
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()

    def mover_inicio(self):
        self.setPixmap(
            QPixmap(self.image).scaled(40, 40))
        self.setGeometry(self.initial_position[0],
                         self.initial_position[1], 40, 40)

    def stop(self):
        self.timer.stop()

    def is_valid_position(self, x, y):
        # Calcula la posición de la celda en el laberinto que comienza en (250, 0)
        cell_x = (x - 250) // 40
        cell_y = y // 40

        if 0 <= cell_x < len(self.laberinto[0]) and 0 <= cell_y < len(self.laberinto):
            return self.laberinto[cell_y][cell_x] != 'P'
        return False

    def animate(self):
        if self.tipo == 'arriba':
            self.mover_arriba()
        elif self.tipo == 'abajo':
            self.mover_abajo()
        elif self.tipo == 'derecha':
            self.mover_derecha()
        elif self.tipo == 'izquierda':
            self.mover_izquierda()
        self.raise_()

    def mover_arriba(self):
        if self.is_valid_position(self.x(), self.y() - 40):
            self.setPixmap(
                QPixmap(self.image).scaled(40, 40))
            self.setGeometry(self.x(), self.y() - 40, 40, 40)
            self.repaint()
        else:
            self.mover_inicio()

    def mover_abajo(self):
        if self.is_valid_position(self.x(), self.y() + 40):
            self.setPixmap(
                QPixmap(self.image).scaled(40, 40))
            self.setGeometry(self.x(), self.y() + 40, 40, 40)
            self.repaint()
        else:
            self.mover_inicio()

    def mover_derecha(self):
        if self.is_valid_position(self.x() + 40, self.y()):
            self.setPixmap(
                QPixmap(self.image).scaled(40, 40))
            self.setGeometry(self.x() + 40, self.y(), 40, 40)
            self.repaint()
        else:
            self.mover_inicio()

    def mover_izquierda(self):
        if self.is_valid_position(self.x() - 40, self.y()):
            self.setPixmap(
                QPixmap(self.image).scaled(40, 40))
            self.setGeometry(self.x() - 40, self.y(), 40, 40)
            self.repaint()
        else:
            self.mover_inicio()
