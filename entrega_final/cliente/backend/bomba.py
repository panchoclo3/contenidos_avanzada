from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, pyqtSignal


class Manzana(QLabel):
    def __init__(self, initial_position: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/manzana_burbuja.png').scaled(40, 40))
        self.setGeometry(initial_position[0], initial_position[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()

    def tipo_bomba(self):
        return 'manzana'


class CongelacionItem(QLabel):
    def __init__(self, initial_position: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/congelacion_burbuja.png').scaled(40, 40))
        self.setGeometry(initial_position[0], initial_position[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()

    def tipo_bomba(self):
        return 'congelacion'


class Bomba(QLabel):

    def __init__(self, laberinto, initial_position: list, congelacion: bool, parent=None):
        super().__init__(parent)
        self.inicio = self.aproximate(initial_position)
        if congelacion:
            self.setPixmap(
                QPixmap('../assets/sprites/congelacion.png').scaled(40, 40))
            self.tipo = 'congelacion'
        else:
            self.setPixmap(
                QPixmap('../assets/sprites/manzana.png').scaled(40, 40))
            self.tipo = 'manzana'
        self.setGeometry(self.inicio[0], self.inicio[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.laberinto = laberinto
        self.direcciones = [
            [-1, 0],  # Arriba
            [0, 1],  # Derecha
            [1, 0],  # Abajo
            [0, -1],  # Izquierda
        ]

        self.show()
        self.raise_()

    def tipo_bomba(self):
        return self.tipo

    def eliminate(self):
        self.hide()
        self.deleteLater()

    def aproximate(self, posicion: tuple):
        return (posicion[0] // 10) * 10, (posicion[1] // 10) * 10

    def es_valida(self, posicion) -> bool:
        if self.laberinto[posicion[0]][posicion[1]] == "P":
            return False

        return True

    def convert(self, x, y):
        cell_x = (x - 250) // 40
        cell_y = y // 40
        return cell_x, cell_y

    def casillas_afectadas(self):
        posiciones = [self.convert(self.x(), self.y())]
        for direccion in self.direcciones:
            posicion = self.convert(self.x(), self.y())

            while True:
                nueva_pos = [posicion[0] + direccion[0],
                             posicion[1] + direccion[1]]

                if self.es_valida(nueva_pos):
                    posiciones.append(nueva_pos)
                    posicion = nueva_pos

                else:
                    break
        return posiciones


class Explosion(QLabel):
    def __init__(self, posicion: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/explosion.png').scaled(40, 40))
        self.posicion = posicion
        self.setGeometry(self.posicion[0], self.posicion[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()


class Congelacion(QLabel):
    def __init__(self, posicion: list, parent=None):
        super().__init__(parent)
        self.setPixmap(
            QPixmap('../assets/sprites/congelacion.png').scaled(40, 40))
        self.posicion = posicion
        self.setGeometry(self.posicion[0], self.posicion[1], 40, 40)
        self.setStyleSheet('background-color: transparent')
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()
