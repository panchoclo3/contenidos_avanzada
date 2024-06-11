import socket
from PyQt5.QtCore import QObject, pyqtSignal
from backend.funciones_cliente import serializar_mensaje, codificar_mensaje, codificar_mensaje2, descodificar_bytes


class Cliente(QObject):
    senal_tablero_recibido = pyqtSignal(list)
    senal_usuario_blockeado = pyqtSignal()
    senal_usuario_permitido = pyqtSignal(str)

    def __init__(self, port, host, disconnect_messaje):
        super().__init__()
        self.port = port
        self.host = host
        self.disconnect_messaje = disconnect_messaje
        self.cliente = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.cliente.connect((self.host, self.port))

    def start(self) -> None:
        try:
            tablero = self.receive_tablero()
            self.senal_tablero_recibido.emit(tablero)
        except KeyboardInterrupt:
            self.close()

    def send(self, msg: str) -> None:
        msg = serializar_mensaje(msg)
        msg = codificar_mensaje(msg)
        msg = codificar_mensaje2(msg)
        self.cliente.send(msg)

    def receive(self) -> bytearray:
        msg = self.cliente.recv(4096)
        mensaje = descodificar_bytes(msg)
        return mensaje

    def recibir_usuario(self) -> str:
        mensaje = self.receive()
        if mensaje:
            self.senal_usuario_permitido.emit(mensaje)
        else:
            self.senal_usuario_blockeado.emit()

    def enviar_usuario(self, usuario: str) -> None:
        self.send(usuario)

    def receive_tablero(self) -> bytearray:
        tablero = []
        usuarios = []
        puntajes = []
        mensaje = self.receive()
        mensaje = mensaje.split(',')
        for i in range(0, len(mensaje), 3):
            usuarios.append(mensaje[i])
            puntajes.append(mensaje[i+2])

        tablero.append(usuarios)
        tablero.append(puntajes)
        return tablero

    def close(self):
        self.send(self.disconnect_messaje)
        print('Cliente desconectado.')
        self.cliente.close()
