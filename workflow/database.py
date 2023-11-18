import json
from datetime import datetime
from os import PathLike
from typing import List, Tuple, Union

import psycopg2
from psycopg2 import Error

from workflow.typing_utils import RequestDict, ResponseDataDict


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

    def create_tables(self):
        """
        Creates the tables in the database.
        """
        with self.connection.cursor() as cur:
            # Create the query_data table with a JSONB column for raw_data
            cur.execute(
                """
                        CREATE TABLE IF NOT EXISTS query_data (
                            id SERIAL PRIMARY KEY,
                            request JSONB,
                            response JSONB
                        )
                    """
            )

            # Create the flights table with a foreign key reference to query_data
            cur.execute(
                """
                        CREATE TABLE IF NOT EXISTS flights (
                            flight_id SERIAL PRIMARY KEY,
                            origin VARCHAR(255),
                            destination VARCHAR(255),
                            flight_departure TIMESTAMP,
                            flight_arrival TIMESTAMP,
                            duration INTERVAL,
                            num_stops INTEGER,
                            company VARCHAR(255),
                            price NUMERIC,
                            query_id INTEGER,
                            FOREIGN KEY (query_id) REFERENCES query_data(id)
                        )
                    """
            )
            self.connection.commit()
            print("Table 'flights' created successfully.")

    def process_queries(
        self, queries: List[Tuple[RequestDict, List[ResponseDataDict]]]
    ):
        """
        Processes the queries and stores the data in the database.
        :param queries: A list of (request, list(responses)) tuples to be stored in the database.
        """
        with self.connection.cursor() as cur:
            for query in queries:
                cur.execute(
                    "INSERT INTO query_data (request, response) VALUES (%s, %s) RETURNING id",
                    (json.dumps(query[0]), json.dumps(query[1])),
                )
                query_id = cur.fetchone()[0]
                for response in query[1]:
                    # i.e. "2024-11-02T09:55:00"
                    format = "%Y-%m-%dT%H:%M:%S"
                    arrival = datetime.strptime(
                        response["itineraries"][0]["segments"][-1]["arrival"]["at"],
                        format,
                    )
                    departure = datetime.strptime(
                        response["itineraries"][0]["segments"][0]["departure"]["at"],
                        format,
                    )
                    cur.execute(
                        """
                        INSERT INTO flights (origin, destination, flight_departure, flight_arrival, duration, num_stops, company, price, query_id) 
                        VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                        """,
                        (
                            response["itineraries"][0]["segments"][0]["departure"][
                                "iataCode"
                            ],
                            response["itineraries"][0]["segments"][-1]["arrival"][
                                "iataCode"
                            ],
                            departure,
                            arrival,
                            arrival - departure,
                            len(response["itineraries"][0]["segments"]) - 1,
                            # carrier company name of only the first flight
                            response["itineraries"][0]["segments"][0]["carrierCode"],
                            response["price"]["total"],
                            query_id,
                        ),
                    )
                print("Query {} stored successfully.".format(query_id))
            self.connection.commit()

    def drop_tables(self):
        """
        Drops the tables in the database.
        """
        with self.connection.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS flights")
            cur.execute("DROP TABLE IF EXISTS query_data")
            self.connection.commit()
            print("Table 'flights' dropped successfully.")
