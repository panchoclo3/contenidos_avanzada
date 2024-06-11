import socket
import json


def usuario_permitido(nombre: str, usuarios_no_permitidos: list[str]) -> bool:
    return nombre not in usuarios_no_permitidos


def usuarios_no_permitidos() -> list[str]:
    with open('usuarios_no_permitidos.txt', 'r') as file:
        data = file.readline()
    data = data.split(',')
    return data


def serializar_mensaje(mensaje: str) -> bytearray:
    return bytearray(mensaje.encode('utf-8'))


def separar_mensaje(mensaje: bytearray) -> list[bytearray]:
    A = []  # 0-5-6
    B = []  # 1-4-7
    C = []  # 2-3-8-9

    lista = ['A', 'B', 'C']
    count = 0
    while count < len(mensaje):
        for element in lista:
            if element == 'A':
                A.append(mensaje[count])
            if element == 'B':
                B.append(mensaje[count])
            if element == 'C':
                C.append(mensaje[count])

            count += 1
            if count >= len(mensaje):
                break

        lista = lista[::-1]

    return [bytearray(A), bytearray(B), bytearray(C)]


def unir_mensaje(mensaje: list[bytearray]) -> bytearray:
    A = mensaje[0]
    B = mensaje[1]
    C = mensaje[2]
    length = len(A) + len(B) + len(C)
    result = bytearray()
    lista = ['A', 'B', 'C']
    count = 0
    while count < length:
        for element in lista:
            if element == 'A':
                result.append(A.pop(0))
            if element == 'B':
                result.append(B.pop(0))
            if element == 'C':
                result.append(C.pop(0))

            count += 1
            if count >= length:
                break

        lista = lista[::-1]
    return result


def encriptar_mensaje(mensaje: bytearray) -> bytearray:
    A, B, C = separar_mensaje(mensaje)
    suma = A[0] + B[-1] + C[0]
    if suma % 2 == 0:
        resultado = '1'.encode('utf-8') + A + C + B

    else:
        resultado = '0'.encode('utf-8') + B + A + C

    return bytearray(resultado)


def desencriptar_mensaje(mensaje: bytearray) -> bytearray:
    length = len(mensaje) - 1
    divider = length // 3
    resto = length % 6
    primero = divider
    segundo = divider
    tercero = divider

    if resto == 1:
        primero += 1
    elif resto == 2:
        primero += 1
        segundo += 1
    elif resto == 4:
        tercero += 1
    elif resto == 5:
        segundo += 1
        tercero += 1
    else:
        pass

    if mensaje[0].to_bytes(1, 'big') == '1'.encode('utf-8'):
        A = mensaje[1:primero+1]
        C = mensaje[primero+1:primero+tercero+1]
        B = mensaje[primero+tercero+1:]

    else:
        B = mensaje[1:segundo+1]
        A = mensaje[segundo+1:segundo+primero+1]
        C = mensaje[segundo+primero+1:]

    return unir_mensaje([A, B, C])


def codificar_mensaje(mensaje: bytearray) -> list[bytearray]:
    mensaje = encriptar_mensaje(mensaje)
    largo = len(mensaje)
    first_block = largo.to_bytes(4, 'big')
    if largo < 36:

        val1 = 1
        second_block = val1.to_bytes(4, 'big')

        val0 = 0
        ceros = val0.to_bytes(36-largo, 'big')
        third_block = mensaje + bytearray(ceros)

        return [bytearray(first_block), bytearray(second_block), third_block]

    cant_bloques = largo // 36
    resto = largo % 36
    last_block = mensaje[-resto:] + bytearray(36-resto)
    result = [bytearray(first_block)]

    for i in range(1, cant_bloques+1):
        numero_block = i.to_bytes(4, 'big')
        result.append(bytearray(numero_block))

        mensaje_cortado = mensaje[(i-1)*36:i*36]
        result.append(mensaje_cortado)

    numero_block = bytearray((cant_bloques+1).to_bytes(4, 'big'))
    result.append(bytearray(numero_block))

    result.append(last_block)
    return result


def codificar_mensaje2(mensaje: list[bytearray]) -> bytes:
    resultado = bytes()
    for block in mensaje:
        resultado += block
    return resultado


def descodificar_bytes(codificado: bytes) -> bytearray:
    first_block = codificado[:4]
    largo = int.from_bytes(first_block, 'big')

    mensaje = bytearray()

    if largo <= 36:
        mensaje += codificado[8:largo+8]

    else:
        block_cant = largo // 36
        resto = largo % 36
        last_block = codificado[48+((block_cant-1)*36)
                                    : resto+48+((block_cant-1)*36)]
        for i in range(block_cant):
            numero_block = codificado[4+(i*36):8+(i*36)]
            mensaje_block = codificado[8+(i*36):44+(i*36)]
            mensaje += mensaje_block
        mensaje += last_block

    mensaje_desencriptado = desencriptar_mensaje(mensaje)
    return mensaje_desencriptado.decode('utf-8')


def descodificar_mensaje(codificado: list[bytearray]) -> bytearray:
    first_block = codificado[0]
    largo = int.from_bytes(first_block, 'big')

    mensaje = bytearray()

    if largo <= 36:
        mensaje += codificado[2]

    else:
        block_cant = largo // 36
        resto = largo % 36
        last_block = codificado[-1]
        for i in range(block_cant):
            mensaje_block = codificado[2+(i*2)]
            mensaje += mensaje_block
        mensaje += last_block

    return desencriptar_mensaje(mensaje)


def usuarios() -> str:
    usuarios = []
    nivel = []
    puntajes = []
    with open('puntaje.txt', 'r') as file:
        data = file.readline()

    return data
