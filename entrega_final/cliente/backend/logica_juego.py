from PyQt6.QtCore import QObject, pyqtSignal
from PyQt6.QtWidgets import QWidget
from backend.conejo import Conejo
from backend.lobos import LoboV, LoboH
from backend.bomba import Bomba, Explosion, Congelacion, CongelacionItem, Manzana
from backend.canon import CanonDown, CanonLeft, CanonRight, CanonUp, Carrot


class Procesador_juego(QObject):

    signal_next_level = pyqtSignal(int)

    def __init__(self):
        super().__init__()
        self.nivel = 1

    def return_nivel(self):
        return self.nivel

    def next_nivel(self):
        self.nivel += 1
        self.start_next_level()

    def start_next_level(self):
        self.signal_next_level.emit(self.nivel)
