import calendar
import datetime
import json
from os import PathLike
from typing import List, Literal, Union

from amadeus import Client, Response, ResponseError

from workflow.utils import Date
from workflow.database import DataBase


class QueryHandler:
    def __init__(
            self,
            api_config_path: Union[str, PathLike],
            db_config_path: Union[str, PathLike],
            log_level: Literal["silent", "warn", "debug"] = "debug",
    ):
        """
        Main Query Handler that uses Amadeus API to collect data on flights, based on the provided config file.
        :param config_path: Path to json config file. See the Amadeus API documentation for available options.
        :param log_level: (optional) the log level of the client, either
            "debug", "warn", or "silent" mode
            (Default: "silent")
        :paramtype log_level: str
        """
        with open(api_config_path) as f:
            config = json.load(f)
        self.amadeus_client = Client(**config, log_level=log_level)
        self.db = DataBase(db_config_path)
        if not self.db.start_db(print_info=True):
            raise Exception("Could not connect to database.")

    def __del__(self):
        """
        Closes the database connection when the QueryHandler object is deleted.
        """
        print("Closing database connection...")
        self.db.close_db()

    def handle_query(self, query_path: Union[str, PathLike]):
        """
        Reads the provided json file and uses the Amadeus API to collect data on flights.
        The json file should contain a list of airports 'cities', a 'date' dict that shows the desired year, month (optional),
         and day (optional), and finally a 'params' dictionary that contains the number of adults
          and other desired parameters for the API call.
          If no month is provided, the API will return data for the entire year.
          If no day is provided, the API will return data for the entire month.
        :param query_path: path to json file containing the query.
        :return:
        """
        with open(query_path) as f:
            query = json.load(f)
            successful_queries = 0
            all_queries = 0
            cities = query["cities"]
            date = query["date"]
            params = query["params"]
            num_cities = len(cities)
            for i in range(num_cities):
                for j in range(num_cities):
                    if i != j:
                        print(
                            "Searching Flighs from {} to {}".format(
                                cities[i], cities[j]
                            )
                        )
                        responses, total_queries = self.get_flight_offers_for_month(
                            cities[i], cities[j], date, params
                        )
                        # print([json.dumps(response.data, indent=4) for response in responses])
                        successful_queries += len(responses)
                        all_queries += total_queries
            print("Successful Queries: {}/{}".format(successful_queries, all_queries))

    def get_flight_offers_for_month(
            self, origin: str, destination: str, date: Date, params: dict
    ) -> tuple[List[Response], int]:
        """
        Gets flight offers for a given date.
        If no month is provided, the API will return data for the entire year.
        If no day is provided, the API will return data for the entire month.
        :param origin: Origin airport code
        :param destination: Destination airport code
        :param date: Date dict containing year, month (optional), and day (optional)
        :param params: Params dict containing the number of adults and other desired parameters for the API call.
        :return:
        """
        year = int(date["year"])
        if date.get("month") is None:
            months = list(range(1, 13))
        else:
            months = [int(date["month"])]
        results = []
        total_queries = 0
        for month in months:
            if date.get("day") is None:
                days = list(range(1, calendar.monthrange(year, month)[1] + 1))
            else:
                days = [int(date["day"])]
            for day in days:
                params["departureDate"] = datetime.date(year, month, day).isoformat()
                print("Date: {}".format(params["departureDate"]))
                total_queries += 1
                try:
                    results.append(
                        self.amadeus_client.shopping.flight_offers_search.get(
                            originLocationCode=origin,
                            destinationLocationCode=destination,
                            **params
                        )
                    )

                except ResponseError as error:
                    # I think that the API can look for flights up to one year from now,
                    # so this error can occur if you try and look too far in the future.
                    # (i.e. today is 2023-11-14, and you try and look for 2024-11-15)
                    print("Error while requesting data: ", error)
        return results, total_queries
