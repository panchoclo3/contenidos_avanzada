from PyQt6.QtCore import QObject, pyqtSignal
from backend.funciones_cliente import validacion_formato


class Procesador_inicio(QObject):

    signal_tablero_procesado = pyqtSignal(list)
    signal_usuario_valido = pyqtSignal(str)
    signal_usuario_invalido = pyqtSignal()
    signal_abrir_ventana_juego = pyqtSignal()

    def __init__(self):
        super().__init__()

    def procesar_tablero(self, tablero: list[list]):
        players, points = tablero
        points = [int(point) for point in points]
        combined_data = list(zip(players, points))
        combined_data.sort(key=lambda x: x[1], reverse=True)
        sorted_players, sorted_points = zip(*combined_data)
        sorted_points = [str(point) for point in sorted_points]
        sorted_data = [list(sorted_players), sorted_points]
        self.signal_tablero_procesado.emit(sorted_data)

    def validar_usuario(self, usuario: str) -> bool:
        if validacion_formato(usuario):
            self.signal_usuario_valido.emit(usuario)
            self.signal_abrir_ventana_juego.emit()
        else:
            self.signal_usuario_invalido.emit()
