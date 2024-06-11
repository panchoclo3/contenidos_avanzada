from PyQt6.QtWidgets import QWidget, QLabel, QPushButton, QGridLayout
from PyQt6.QtGui import QPixmap
from PyQt6.QtCore import QTimer, pyqtSignal, Qt, QMutex
from frontend.clases_graficas import Imagen, Etiqueta, Caja, Boton, Inventario, Perdiste, ManzanaItem, CongelacionItem, Ganaste
from backend.canon import CanonDown, CanonLeft, CanonRight, CanonUp, Carrot
from backend.bomba import Bomba, Explosion, Congelacion, CongelacionItem, Manzana
from backend.lobos import LoboV, LoboH
from backend.conejo import Conejo
from backend.bloque import Bloque


class VentanaJuego(QWidget):

    signal_level_ended = pyqtSignal()

    def __init__(self, parent=None):
        super().__init__(parent)
        self.inicializa_gui()

    def inicializa_gui(self):
        """Inicializa la interfaz gráfica de la ventana del juego."""
        self.setGeometry(300, 150, 890, 640)
        self.setWindowTitle('DCConejoChico')
        self.setStyleSheet('background-color: pink')
        self.tiempo = 120
        self.temporizador = Etiqueta(
            f'Tiempo: {self.tiempo}', 20, (20, 30), self)
        self.vidas = 3
        self.vidas_label = Etiqueta(
            f'Vidas restantes: {self.vidas}', 20, (20, 60), self)

        self.boton = Boton('Salir', (20, 100), self)
        self.boton.clicked.connect(self.close)

        self.boton = Boton('Pausa', (150, 100), self)
        self.boton.clicked.connect(self.pause_control)

        self.inventario_imagen = Inventario((20, 150), self)
        self.manzanas = 0
        self.congelaciones = 0
        self.manzanaIcon = ManzanaItem((20, 20), self.inventario_imagen)
        self.manzana_label = Etiqueta(
            f'X {self.manzanas}', 20, (100, 50), self.inventario_imagen)
        self.congelacionIcon = CongelacionItem(
            (20, 120), self.inventario_imagen)
        self.congelacion_label = Etiqueta(
            f'X {self.congelaciones}', 20, (100, 130), self.inventario_imagen)

        self.inventario = []
        self.laberintos = ['../assets/laberintos/tablero_1.txt',
                           '../assets/laberintos/tablero_2.txt',
                           '../assets/laberintos/tablero_3.txt']
        self.lock = QMutex()

        self.chose_level(1)

    def chose_level(self, nivel) -> None:
        """Cambia el nivel del juego y carga un nuevo laberinto.
        """
        if nivel == 1:
            pass
        else:
            self.clear_level()
        self.nivel = nivel
        self.load_level(self.laberintos[nivel - 1])

    def clear_level(self) -> None:
        """Limpia todos los elementos del nivel actual."""
        for entidad in self.entidades_enemigas:
            entidad.eliminate()
        for entidad in self.entidades_bombas:
            entidad.eliminate()
        for entidad in self.entidades_explosiones:
            entidad.eliminate()
        self.conejo.eliminate()
        for bloque in self.bloques:
            bloque.eliminate()

    def load_level(self, file_path) -> None:
        """Carga un nuevo nivel a partir de un archivo de laberinto.
        """
        self.vidas_afectadas = True
        self.pause = False
        self.bomba_step = 0
        self.entidades_enemigas = []
        self.entidades_bombas = []
        self.entidades_explosiones = []
        self.bloques = []
        self.cheat_kil = []
        self.cheat_inf = []

        self.laberinto = self.cargar_laberinto(file_path)
        self.load_laberinto(self.laberinto)
        self.conejo.raise_()
        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.actualizar_tiempo)
        self.timer.start()
        self.timer_coliciones_conejo()

    def timer_coliciones_conejo(self) -> None:
        """Configura y activa el temporizador para detectar colisiones con el conejo."""
        self.timer_c = QTimer(self)
        self.timer_c.setInterval(100)
        self.timer_c.timeout.connect(self.coliciones_conejo)
        self.timer_c.start()

    def timer_coliciones_explosion(self) -> None:
        """Configura y activa el temporizador para detectar colisiones con explosiones."""
        self.timer_e = QTimer(self)
        self.timer_e.setInterval(1000)
        self.timer_e.timeout.connect(self.coliciones_explosion)
        self.timer_e.start()

    def coliciones_explosion(self) -> None:
        """Detecta colisiones entre enemigos y explosiones y elimina los enemigos afectados."""
        for lobo in self.entidades_enemigas:
            coordenadas = [lobo.x(), lobo.y()]
            coordenadas = self.convert_pixels_coo(
                coordenadas[0], coordenadas[1])
            if coordenadas in self.casillas_afectadas:
                lobo.eliminate()
                self.entidades_enemigas.remove(lobo)

    def timer_bombas(self) -> None:
        """Configura y activa el temporizador para gestionar bombas y explosiones."""
        self.timer_bomba = QTimer(self)
        self.timer_bomba.setInterval(5000)
        if self.bomba.tipo == 'manzana':
            self.timer_bomba.timeout.connect(self.explosion_animation)
        else:
            self.timer_bomba.timeout.connect(self.congelacion_animation)
        self.timer_bomba.start()

    def explosion_animation(self) -> None:
        """Realiza la animación de una explosión."""
        self.lock.lock()
        try:
            if self.bomba_step == 0:
                self.bomba.eliminate()
                for casilla in self.casillas_afectadas:
                    casilla = [casilla[0] * 40 + 250, casilla[1] * 40]
                    self.explosion = Explosion(casilla, self)
                    self.entidades_explosiones.append(self.explosion)
                self.bomba_step += 1
                self.timer_coliciones_explosion()
            elif self.bomba_step == 1:
                self.timer_bomba.stop()
                self.timer_e.stop()
                for bomba in self.entidades_explosiones:
                    bomba.eliminate()
                    self.entidades_explosiones.remove(bomba)
                self.bomba_step = 0
        finally:
            self.lock.unlock()

    def congelacion_animation(self) -> None:
        """Realiza la animación de la congelación."""
        if self.bomba_step == 0:
            self.bomba.eliminate()
            for casilla in self.casillas_afectadas:
                casilla = [casilla[0] * 40 + 250, casilla[1] * 40]
                self.congelacion = Congelacion(casilla, self)
                self.entidades_explosiones.append(self.congelacion)
            self.bomba_step += 1
        elif self.bomba_step == 1:
            for bomba in self.entidades_explosiones:
                bomba.eliminate()
                self.entidades_explosiones.remove(bomba)
            self.bomba_step = 0
            self.timer_bomba.stop()

    def pause_control(self) -> None:
        """Controla la pausa del juego."""
        if not self.pause:
            self.timer.stop()
            for enemigo in self.entidades_enemigas:
                enemigo.timer.stop()
        else:
            self.timer.start()
            for enemigo in self.entidades_enemigas:
                enemigo.timer.start()
        self.pause = not self.pause

    def actualizar_tiempo(self) -> None:
        """Actualiza el tiempo restante del juego y verifica si se ha agotado el tiempo."""
        self.tiempo -= 1
        self.temporizador.setText(f'Tiempo: {self.tiempo}')
        self.temporizador.repaint()
        if self.tiempo == 0:
            self.timer.stop()
            self.pause_control()
            self.perdiste = Perdiste(self)
        if len(self.cheat_kil) >= 3:
            self.cheat_kil = []
        if len(self.cheat_inf) >= 3:
            self.cheat_inf = []

    def cargar_laberinto(self, file_path) -> list:
        """Carga un laberinto desde un archivo."""
        laberinto = []
        with open(file_path, 'r') as file:
            for line in file:
                file = line.strip().split(',')
                laberinto.append(file[:-1])
        return laberinto

    def load_laberinto(self, laberinto) -> None:
        """Carga un laberinto en la interfaz gráfica."""
        y_axis = 0
        x_axis = 250

        for row in laberinto:
            for element in row:
                if element == 'P':
                    self.bloque = Bloque([x_axis, y_axis], True, self)
                    self.bloques.append(self.bloque)
                else:
                    self.bloque = Bloque([x_axis, y_axis], False, self)
                    self.bloques.append(self.bloque)
                    if element == 'LV':
                        self.lobo_v = LoboV(self.laberinto,
                                            [x_axis, y_axis], self)
                        self.entidades_enemigas.append(self.lobo_v)
                    elif element == 'LH':
                        self.lobo_h = LoboH(
                            self.laberinto, [x_axis, y_axis], self)
                        self.entidades_enemigas.append(self.lobo_h)

                    elif element == 'C':
                        self.conejo = Conejo(
                            self.laberinto, [x_axis, y_axis], self)
                        self.punto_inicio = [x_axis, y_axis]

                    elif element == 'S':
                        self.salida = [x_axis, y_axis]

                    elif element == 'BM':
                        self.manzana = Manzana([x_axis, y_axis], self)
                        self.entidades_bombas.append(self.manzana)
                    elif element == 'BC':
                        self.congelacion = CongelacionItem(
                            [x_axis, y_axis], self)
                        self.entidades_bombas.append(self.congelacion)
                    elif element == 'CD':
                        self.canon = CanonDown([x_axis, y_axis], self)
                        self.carrot = Carrot(self.laberinto, 'abajo', [
                                             x_axis, y_axis + 40], self)
                        self.entidades_enemigas.append(self.carrot)

                    elif element == 'CU':
                        self.canon = CanonUp([x_axis, y_axis], self)
                        self.carrot = Carrot(self.laberinto, 'arriba', [
                                             x_axis, y_axis - 40], self)
                        self.entidades_enemigas.append(self.carrot)

                    elif element == 'CL':
                        self.canon = CanonLeft([x_axis, y_axis], self)
                        self.carrot = Carrot(self.laberinto, 'izquierda', [
                                             x_axis - 40, y_axis], self)
                        self.entidades_enemigas.append(self.carrot)

                    elif element == 'CR':
                        self.canon = CanonRight([x_axis, y_axis], self)
                        self.carrot = Carrot(self.laberinto, 'derecha', [
                                             x_axis + 40, y_axis], self)
                        self.entidades_enemigas.append(self.carrot)

                x_axis += 40
            x_axis = 250
            y_axis += 40

    def keyPressEvent(self, event) -> None:
        """Controla el movimiento del conejo y la interacción con los elementos del juego."""
        if event.key() == Qt.Key.Key_W:
            self.conejo.animate('up')
        elif event.key() == Qt.Key.Key_S:
            self.conejo.animate('down')
        elif event.key() == Qt.Key.Key_A:
            self.conejo.animate('left')
        elif event.key() == Qt.Key.Key_D:
            self.conejo.animate('right')
        elif event.key() == Qt.Key.Key_G:
            self.pick_bomba()
        elif event.key() == Qt.Key.Key_K:
            self.cheat_kil.append('K')
        elif event.key() == Qt.Key.Key_I:
            self.cheat_kil.append('I')
            self.cheat_inf.append('I')
        elif event.key() == Qt.Key.Key_L:
            self.cheat_kil.append('L')
            if self.cheat_kil == ['K', 'I', 'L']:
                self.eliminate_all_enemies()
                self.cheat_kil = []
        elif event.key() == Qt.Key.Key_N:
            self.cheat_inf.append('N')
        elif event.key() == Qt.Key.Key_F:
            self.cheat_inf.append('F')
            if self.cheat_inf == ['I', 'N', 'F']:
                self.infinitas_vidas()

    def eliminate_all_enemies(self) -> None:
        """Elimina a todos los enemigos del juego."""
        self.lock.lock()
        try:
            for entidad in list(self.entidades_enemigas):
                entidad.stop()
                entidad.eliminate()
                self.entidades_enemigas.remove(entidad)
        finally:
            self.lock.unlock()

        self.cheat_kil = []
        self.cheat_inf = []

    def infinitas_vidas(self) -> None:
        """Otorga vidas infinitas al conejo."""
        self.vidas_afectadas = False
        self.vidas = 350
        self.vidas_label.setText(f'Vidas restantes: {self.vidas}')
        self.vidas_label.repaint()
        self.vidas_label.repaint()
        self.cheat_kil = []
        self.cheat_inf = []
        self.timer.stop()

    def put_bomba(self, event) -> None:
        """Controla la interacción del conejo con los elementos del juego."""
        # no esta terminado, AttributeError: 'QMouseEvent' object has no attribute 'x'
        if self.manzanas == 0 and self.congelaciones == 0:
            pass
        else:
            if self.manzanas != 0:
                self.bomba = Bomba(
                    self.laberinto, event, False, self)
                self.manzanas -= 1
                self.manzana_label.setText(f'X {self.manzanas}')
                self.manzana_label.repaint()
            else:
                self.bomba = Bomba(
                    self.laberinto, event, True, self)
                self.congelaciones -= 1
                self.congelacion_label.setText(f'X {self.congelaciones}')
                self.congelacion_label.repaint()
            self.casillas_afectadas = self.bomba.casillas_afectadas()
            self.timer_bombas()

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            event_x = int(event.position().x())
            event_y = int(event.position().y())
            if event_x >= 250:
                self.put_bomba([event_x, event_y])
        else:
            pass

    def pick_bomba(self):
        """Permite al conejo recoger una bomba."""
        for bomba in self.entidades_bombas:
            if self.conejo.x() == bomba.x() and self.conejo.y() == bomba.y():
                if bomba.tipo_bomba() == 'congelacion':
                    self.congelaciones += 1
                    self.congelacion_label.setText(f'X {self.congelaciones}')
                    self.congelacion_label.repaint()
                else:
                    self.manzanas += 1
                    self.manzana_label.setText(f'X {self.manzanas}')
                    self.manzana_label.repaint()

                self.entidades_bombas.remove(bomba)
                bomba.eliminate()

    def convert_pixels_coo(self, x, y) -> list:
        """Convierte coordenadas de píxeles a coordenadas de celdas."""
        cell_x = (x - 250) // 40
        cell_y = y // 40
        return cell_x, cell_y

    def convert_coo_pixels(self, x, y) -> list:
        """Convierte coordenadas de celdas a coordenadas de píxeles."""
        cell_x = x * 40 + 250
        cell_y = y * 40
        return cell_x, cell_y

    def coliciones_conejo(self) -> None:
        """Detecta colisiones entre el conejo y los enemigos."""
        for entidad in self.entidades_enemigas:
            if self.conejo.colision(entidad):
                self.conejo_a_entrada()
                if self.vidas_afectadas:
                    self.vidas -= 1
                else:
                    pass
                self.vidas_label.setText(f'Vidas restantes: {self.vidas}')
                self.vidas_label.repaint()
                if self.vidas == 0:
                    self.timer.stop()
                    self.perdiste = Perdiste(self)
                    self.pause_control()
                else:
                    pass
        self.conejo_en_salida()

    def conejo_a_entrada(self):
        """Reposiciona al conejo en la entrada del laberinto."""
        self.conejo.setPixmap(
            QPixmap('../assets/sprites/conejo.png').scaled(40, 40))
        self.conejo. setGeometry(
            self.punto_inicio[0], self.punto_inicio[1], 40, 40)

    def conejo_en_salida(self):
        """Verifica si el conejo se encuentra en la salida del laberinto, y si es así, emite la señal para el siguiente nivel."""
        if [self.conejo.x(), self.conejo.y()] == self.salida:
            if self.nivel == 3:
                self.timer.stop()
                self.ganaste = Ganaste(self)
            else:
                self.signal_level_ended.emit()
                self.timer.stop()
