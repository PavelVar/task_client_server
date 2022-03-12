"""
Module contains MessengerServer class.
This class organize server functioning using separate threads for incoming connections.
"""

import socket
import logging
import threading
from socket import SocketType

import variables
from messenger_handler import ClientMessengerHandler
from messenger_server_data_base_manager import MessengerServerDataBase


class MessengerServer:
    """
    Class MessengerServer creates sockets, separate threads for them and manages incoming messages from clients.
    """
    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='[%d.%m.%Y - %H:%M:%S]', level=logging.INFO)

    def __init__(self, host: str, port: int):
        self.host = host
        self.port = port
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.db = MessengerServerDataBase()

    def start(self):
        """Organize socket creation and start."""
        self.create_server_socket()

        while True:
            client = self.accept_client_connection()
            thread = threading.Thread(target=self.serve_client, args=(client,))
            thread.start()

    def create_server_socket(self):
        """Connect socket to host and port."""
        self.server_socket.bind(('', self.port))
        self.server_socket.listen()
        logging.info(f'Server is running on {self.host}:{self.port}')

    def accept_client_connection(self) -> SocketType:
        """Accepts clients connections."""
        client, client_address = self.server_socket.accept()
        logging.info(f'connected: {client}')
        return client

    def serve_client(self, client: SocketType):
        """Manages commands from clients using messages_handler."""

        client.send(variables.start_message.encode())
        sqlite_connection = self.db.connect(variables.database_name)
        logging.info('Connection to db created')
        table_name = variables.table_name
        self.db.table_create(sqlite_connection, table_name)
        logging.info(f'Table created {table_name}')
        while True:

            try:
                incoming_data = client.recv(1024).decode()
                messages_handler = ClientMessengerHandler(client)
                if incoming_data not in variables.proper_incoming_data:
                    client.send(variables.close_message.encode())
                    messages_handler.session_close()
                    break
            except (ConnectionAbortedError, ConnectionResetError):
                logging.error('Connection closed.')
                return False

            messages_handler.manage_clients_queries(incoming_data, self.db, sqlite_connection, table_name)



