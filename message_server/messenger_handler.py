"""
Module contains class Helper which handles operations for MessengerServer.
"""
import logging
from socket import SocketType
from sqlite3 import Connection

import variables
from messenger_server_data_base_manager import MessengerServerDataBase


class ClientMessengerHandler:
    """
    Class ClientMessengerHandler handles operations for MessengerServer while contacting with clients.
    """

    logging.basicConfig(format='%(asctime)s - %(message)s', datefmt='[%d.%m.%Y - %H:%M:%S]', level=logging.INFO)
    clients_online = {}

    def __init__(self, client: SocketType):
        self.client = client

    def session_close(self):
        """Closes session."""
        logging.info(f'Connection closed for {self.client}')
        if self.client in self.clients_online:
            del self.clients_online[self.client]
        self.client.close()

    def manage_clients_queries(self, incoming_data: str,
                               db: MessengerServerDataBase, sqlite_connection: Connection, table_name: str):
        """Helps server manage main stream of clients queries"""

        if incoming_data == '-reg':
            existing_users = db.list_user_names(sqlite_connection, table_name)
            login, password = self.register_client(existing_users)
            db.insert_data(sqlite_connection, table_name, login, password)
            logging.info(f'New info added to db: login-"{login}".')
            self.client.send(variables.success_register_message.encode())

        elif incoming_data == '-log':
            logins_and_passwords = db.list_user_names_and_passwords(sqlite_connection, table_name)
            self.log_in(logins_and_passwords)
            self.message_manager()

    def register_client(self, existing_users: list) -> tuple:
        """Saves login and password of the new users after their registration."""
        self.client.send(variables.enter_login_message.encode())
        login = self.client.recv(1024).decode()

        while login in existing_users:
            self.client.send(variables.error_log_message.encode())
            login = self.client.recv(1024).decode()

        self.client.send(variables.enter_password_message.encode())
        password = self.client.recv(1024).decode()
        logging.info(f'New client registered: login-"{login}".')
        return login, password

    def log_in(self, logins_and_passwords: dict):
        """Checks login and password of the user to log him in."""
        self.client.send(variables.enter_login_message.encode())
        login = self.client.recv(1024).decode()

        while login not in logins_and_passwords.keys():
            self.client.send(variables.error_log_message.encode())
            login = self.client.recv(1024).decode()

        self.client.send(variables.enter_password_message.encode())
        password = self.client.recv(1024).decode()

        while password != logins_and_passwords[login]:
            self.client.send(variables.error_password_message.encode())
            password = self.client.recv(1024).decode()

        self.client.send(variables.success_login_message.encode())
        logging.info(f'New client logged in: login-"{login}".')
        self.clients_online[self.client] = login

    def message_manager(self):
        """Manages user messages after registration and logging."""
        self.client.send(variables.messages_option.encode())

        while True:
            try:
                data = self.client.recv(1024).decode()
                data = data.lstrip('-')
                data = data.split(' ', 1)
                if len(data) > 1:
                    command, message = data[0], data[1]
                else:
                    command, message = data[0], 'Empty message'

                if command == '2all':
                    self.send_massage_to_all(message)
                elif command == 'show':
                    self.show_clients_online()
                elif command in self.clients_online.values():
                    self.message_to_one(command, message)
                elif command == 'exit':
                    self.session_close()
                    break
                else:
                    self.client.send(variables.mistake.encode())
            except (ConnectionAbortedError, ConnectionResetError):
                logging.error('Connection closed.')
                return False

    def send_massage_to_all(self, message: str):
        """Sends message to all users/"""
        for current_client in self.clients_online:
            if current_client != self.client:
                current_client.send(message.encode())
        logging.info(f'{self.client} sent message "{message}" too all.')
        self.message_manager()

    def message_to_one(self, recipient: str, message: str):
        """Sends message to one user according to client's query."""
        for client, login in self.clients_online.items():
            if login == recipient:
                client.send(message.encode())
                logging.info(f'{client} sent message "{message}" too "{recipient}".')
        self.message_manager()

    def show_clients_online(self):
        list_of_clients_online = [client for client in self.clients_online.values()]
        self.client.send(f'Now online: {list_of_clients_online}'.encode())
        self.message_manager()
