import json
from os import PathLike
from typing import Union

import psycopg2
from psycopg2 import Error


class DataBase:
    """
    A simple class for connecting to a PostgreSQL database.

    Usage:

    db = DataBase(db_config_path)

    if not db.start_db(print_info=True):
        raise Exception("Could not connect to database.")

    # Do stuff with the database

    db.close_db()
    """

    def __init__(self, config_path: Union[str, PathLike]):
        with open(config_path) as f:
            self._config = json.load(f)

    def start_db(self, print_info: bool = True):
        """
        Starts the database connection.
        :param print_info: (optional) boolean flag, whether to print detailed information about the connection.
        :return: True if the connection was successful, otherwise false.
        """
        try:
            # Connect to an existing database
            self.connection = psycopg2.connect(**self._config)
            # Create a cursor to perform database operations
            self.cursor = self.connection.cursor()
            if print_info:
                # Print PostgreSQL details
                print("PostgreSQL server information")
                print(self.connection.get_dsn_parameters(), "\n")
                # Executing a SQL query
                self.cursor.execute("SELECT version();")
                # Fetch result
                record = self.cursor.fetchone()
                print("You are connected to - ", record, "\n")
        except (Exception, Error) as error:
            if print_info:
                print("Error while connecting to PostgreSQL", error)
            return False
        return True

    def close_db(self):
        """
        Closes the database connection.
        """
        if self.connection:
            self.cursor.close()
            self.connection.close()
            print("PostgreSQL connection is closed")
        else:
            print("No connection to close.")

    def add_element(self, row):
        pass

    def add_elements(self, rows):
        pass

    def remove_element(self, row_id):
        pass

    def remove_elements(self, row_ids):
        pass

    def get_element(self, row_id):
        pass

    def get_elements(self, row_ids):
        pass
