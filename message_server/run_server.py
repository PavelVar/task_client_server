import socket

import variables
from messenger_server import MessengerServer


if __name__ == '__main__':
    server = MessengerServer(socket.gethostbyname(socket.gethostname()), variables.port_num)
    server.start()
