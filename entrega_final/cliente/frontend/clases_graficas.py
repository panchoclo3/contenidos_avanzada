from PyQt6.QtWidgets import (
    QApplication, QWidget, QLabel, QPushButton, QLineEdit, QMainWindow, QVBoxLayout, QFrame)
from PyQt6.QtGui import QPixmap


class Boton(QPushButton):
    def __init__(self, text, position: tuple, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            'font-size: 15px; font-family: Courier; color: #E728A4')
        self.resize(90, 30)
        self.move(position[0], position[1])


class Caja(QLineEdit):
    def __init__(self, position: tuple, parent=None):
        super().__init__(parent)
        self.setStyleSheet(
            'font-size: 20px; font-family: Courier; color: #E728A4')
        self.resize(300, 40)
        self.move(position[0], position[1])


class Etiqueta(QLabel):
    def __init__(self, text, font_size, position: tuple, parent=None):
        super().__init__(text, parent)
        self.setStyleSheet(
            'font-size: {}px; font-family: Courier; color: #E728A4'.format(font_size))
        self.move(position[0], position[1])


class Imagen(QLabel):
    def __init__(self, path, position: tuple, scale: tuple, parent=None):
        super().__init__(parent)
        scale_x = scale[0]
        scale_y = scale[1]
        self.setPixmap(QPixmap(path).scaled(scale_x, scale_y))
        self.move(position[0], position[1])
        self.raise_()

    def eliminate(self):
        self.hide()


class Tablero(QFrame):
    def __init__(self, position: tuple, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color: pink')
        self.move(position[0], position[1])
        self.resize(400, 220)
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Raised)
        self.setLineWidth(5)
        self.setMidLineWidth(5)

    def display(self, players, points):
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.setLayout(self.layout)
        count = 1
        self.layout.addWidget(Etiqueta(
            '        Salon de la fama', 20, (0, 0), self))
        for player, point in zip(players, points):
            self.layout.addWidget(Etiqueta(
                f'         {count}. {player}: {point} puntos', 15, (0, 0), self))
            count += 1


class Inventario(QFrame):
    def __init__(self, position: tuple, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color: lightblue')
        self.move(position[0], position[1])
        self.resize(220, 460)
        self.setFrameShape(QFrame.Shape.Box)
        self.setFrameShadow(QFrame.Shadow.Sunken)
        self.setLineWidth(3)
        self.setMidLineWidth(3)


class ManzanaItem(QLabel):
    def __init__(self, position: tuple, parent=None):
        super().__init__(parent)
        self.setPixmap(QPixmap('../assets/sprites/manzana.png').scaled(70, 70))
        self.move(position[0], position[1])
        self.show()


class CongelacionItem(QLabel):
    def __init__(self, position: tuple, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/congelacion.png').scaled(70, 70))
        self.move(position[0], position[1])
        self.show()


class Perdiste(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color: #E728A4')
        self.resize(400, 200)
        self.move(500, 300)
        self.setWindowTitle('Perdiste')
        self.label = QLabel('Perdiste', self)
        self.label.setStyleSheet(
            'font-size: 50px; font-family: Courier; color: white')
        self.label.move(120, 50)
        self.label.show()
        self.show()


class Ganaste(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet('background-color: #E728A4')
        self.resize(400, 200)
        self.move(500, 300)
        self.setWindowTitle('Ganaste')
        self.label = QLabel('Ganaste', self)
        self.label.setStyleSheet(
            'font-size: 50px; font-family: Courier; color: white')
        self.label.move(120, 50)
        self.label.show()
        self.show()
