from PyQt6.QtWidgets import QLabel
from PyQt6.QtGui import QPixmap


class Bloque(QLabel):

    def __init__(self, position: list, pared: bool, parent=None):
        super().__init__(parent)
        self.pared = pared
        self.x_axis = position[0] // 40
        self.y_axis = position[1] // 40
        if pared:
            self.setPixmap(
                QPixmap('../assets/sprites/bloque_pared.jpeg').scaled(40, 40))
        else:
            self.setPixmap(
                QPixmap('../assets/sprites/bloque_fondo.jpeg').scaled(40, 40))
        self.move(position[0], position[1])
        self.show()

    def eliminate(self):
        self.hide()
        self.deleteLater()
