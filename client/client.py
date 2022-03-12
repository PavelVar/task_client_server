"""
Module contains class Client for interaction with server by socket. Client could receive and send messages.
"""

import socket
import sys
import logging
from typing import Tuple


class MessangerClient:
    """Class Client contains methods (receive, send) for client to organize his connection to the server."""
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='[%d.%m.%Y - %H:%M:%S]', level=logging.INFO)

    def __init__(self, server_address: Tuple[str, int]):
        self.server_address = server_address
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def start(self):
        """Connects to server by socket and creates new thread."""
        self.client_socket.connect(self.server_address)
        logging.info('<<<Anytime you want to exit - input "-exit" and press enter>>>\n')
        self.receive_message()

    def receive_message(self):
        """Await and prints incoming messages."""
        while True:
            message = self.client_socket.recv(1024).decode()
            logging.info(message)
            self.send_message()

    def send_message(self):
        """Sends messages to the server."""
        while True:
            message = input()
            if message == '-exit':
                self.exit_from_client()
            else:
                self.client_socket.send(message.encode())
                self.receive_message()

    @staticmethod
    def exit_from_client():
        """Closes connection"""
        logging.info('You have closed connection\n')
        sys.exit(0)
