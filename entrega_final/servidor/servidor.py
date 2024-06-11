import sys
import socket
from PyQt6.QtCore import pyqtSignal, QObject
from funciones_servidor import descodificar_bytes, usuarios, serializar_mensaje, codificar_mensaje, descodificar_mensaje, codificar_mensaje2, usuario_permitido, usuarios_no_permitidos


class Servidor(QObject):

    def __init__(self, port, host, disconect_menssaje) -> None:
        super().__init__()
        self.port = port
        self.host = host
        self.disconect_menssaje = disconect_menssaje
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((self.host, self.port))

    def recibir_mensaje(self, conn) -> bytearray:
        msg = conn.recv(4096)
        if msg:
            msg = descodificar_bytes(msg)
            return msg
        return None

    def send(self, msg: str, conn) -> None:
        msg = serializar_mensaje(msg)
        msg = codificar_mensaje(msg)
        msg = codificar_mensaje2(msg)
        conn.send(msg)

    def handle_client(self, conn, addr):
        print(f"[NUEVA CONEXIÓN] {addr} conectado.")
        connected = True

        mensaje = usuarios()
        self.send(mensaje, conn)

        while connected:
            msg = self.recibir_mensaje(conn)
            if msg:
                if msg == self.disconect_menssaje:
                    connected = False
                else:
                    print(f"[{addr}] {msg}")
            else:
                pass

        print(f"[DESCONEXIÓN] {addr} desconectado.")
        conn.close()

    def start(self):
        self.server.listen()
        print("Servidor aceptando conexiones en el puerto", self.port)
        while True:
            try:
                conn, addr = self.server.accept()
                self.handle_client(conn, addr)

            except KeyboardInterrupt:
                print("Servidor cerrado.")
                sys.exit()

    def recibir_usuario(self, conn) -> bytearray:
        usuario = self.recibir_mensaje(conn)
        usuario_no_permitido = usuarios_no_permitidos()
        if usuario_permitido(usuario, usuario_no_permitido):
            return usuario
