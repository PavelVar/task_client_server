"""Module contains class DataBase for operations with database for messenger_server.py.
"""
import sqlite3
from sqlite3 import Connection


class MessengerServerDataBase:
    """
    Class DataBase provides methods for operations with sqlite3
    """

    @staticmethod
    def connect(db_name: str):
        """Creates connection to provided database."""
        sqlite_connection = sqlite3.connect(db_name)
        return sqlite_connection

    @staticmethod
    def table_create(connection: Connection, table_name: str):
        """Creates table and columns in the database."""
        cursor = connection.cursor()
        cursor.execute(f'CREATE TABLE if not exists {table_name} {"(login text PRIMARY KEY, password text)"}')
        connection.commit()

    @staticmethod
    def list_user_names(connection: Connection, table_name: str) -> list:
        """Selects names (logins) of existing users: data from column 'login'."""
        cursor = connection.cursor()
        user_logins = [login[0] for login in cursor.execute(f'SELECT "login" FROM {table_name}')]
        return user_logins

    @staticmethod
    def insert_data(connection: Connection, table_name: str, login: str, password: str):
        """Insert clients login and password to the table."""
        cursor = connection.cursor()
        cursor.execute(f'INSERT INTO {table_name} {"(login, password)"} VALUES ("{login}", "{password}")')
        connection.commit()

    @staticmethod
    def list_user_names_and_passwords(connection: Connection, table_name: str) -> dict:
        """Insert clients login and password to the table."""
        cursor = connection.cursor()
        user_logins_and_names = {login: password for login, password in cursor.execute(f'SELECT * FROM {table_name}')}
        return user_logins_and_names
