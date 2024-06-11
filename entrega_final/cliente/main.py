from backend.funciones_cliente import read_config
import sys
import json
import os

from PyQt6.QtWidgets import QApplication

from backend.cliente import Cliente
from backend.logica_inicio import Procesador_inicio
from backend.logica_juego import Procesador_juego
from frontend.ventana_inicio import VentanaInicio
from frontend.ventana_juego import VentanaJuego

config = read_config()
HOST = config['host']
DISCONNECT_MESSAGE = config['disconnect_message']
PORT = int(sys.argv[1])


class Juego():

    def __init__(self) -> None:
        self.ventana_inicio = VentanaInicio()
        self.ventana_juego = VentanaJuego()
        self.datos_usuario = []

        self.procesador_juego = Procesador_juego()
        self.procesador_inicio = Procesador_inicio()

        self.cliente = Cliente(PORT, HOST, DISCONNECT_MESSAGE)

        self.conecciones()
        self.cliente.start()
        self.ventana_inicio.show()

    def conecciones(self):
        # conecciones ventana inicio
        self.ventana_inicio.signal_usuario.connect(
            self.procesador_inicio.validar_usuario)
        self.ventana_inicio.signal_cerrar.connect(self.cliente.close)
        # conneciones cliente
        self.cliente.senal_tablero_recibido.connect(
            self.procesador_inicio.procesar_tablero)
        self.cliente.senal_usuario_blockeado.connect(
            self.ventana_inicio.usuario_blockeado)
        self.cliente.senal_usuario_permitido.connect(self.abrir_ventana_juego)
        # conecciones procesador inicio
        self.procesador_inicio.signal_tablero_procesado.connect(
            self.ventana_inicio.display_tablero)
        self.procesador_inicio.signal_usuario_valido.connect(
            self.cliente.send)
        self.procesador_inicio.signal_usuario_invalido.connect(
            self.ventana_inicio.usuario_invalido)
        self.procesador_inicio.signal_abrir_ventana_juego.connect(
            self.abrir_ventana_juego)
        # conecciones ventana juego
        self.ventana_juego.signal_level_ended.connect(
            self.procesador_juego.next_nivel)

        # conecciones procesador juego
        self.procesador_juego.signal_next_level.connect(
            self.ventana_juego.chose_level)

    def abrir_ventana_juego(self):
        self.ventana_inicio.close()
        self.ventana_juego.show()


if __name__ == '__main__':
    app = QApplication(sys.argv)
    juego = Juego()
    sys.exit(app.exec())
