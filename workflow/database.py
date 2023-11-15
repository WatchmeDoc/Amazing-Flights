import psycopg2
import json
from psycopg2 import Error


class DataBase:
    def __init__(self, config_path, ):
        with open(config_path) as f:
            self._config = json.load(f)

    def start_db(self, print_info=True):
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
