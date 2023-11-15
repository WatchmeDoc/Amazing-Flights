import argparse

from workflow.query_handler import QueryHandler

if __name__ == "__main__":
    parser = argparse.ArgumentParser("Workflow to collect data on flights.")
    parser.add_argument(
        "-a",
        "--apiconfig",
        type=str,
        help="Path to Amadeus API config file.",
        default="workflow/configs/api_config.json",
    )
    parser.add_argument(
        "-d",
        "--dbconfig",
        type=str,
        help="Path to Database config file.",
        default="workflow/configs/dbconfig.json",
    )
    parser.add_argument(
        "-q",
        "--query",
        type=str,
        help="Path to query json file.",
        default="workflow/flight_queries/example.json",
    )
    args = parser.parse_args()
    query_handler = QueryHandler(
        api_config_path=args.apiconfig, db_config_path=args.dbconfig
    )
    query_handler.handle_query(query_path=args.query)
