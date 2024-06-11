import sys
import json
from servidor import Servidor

with open('config.json', 'r') as f:
    data = json.load(f)
    HOST = data['host']
    HEADER = data['header']
    FORMAT = data['format']
    DISCONNECT_MESSAGE = data['disconnect_message']

PORT = int(sys.argv[1])

if __name__ == '__main__':
    servidor = Servidor(PORT, HOST, DISCONNECT_MESSAGE)
    servidor.start()
