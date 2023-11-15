from workflow.query_handler import QueryHandler

if __name__ == "__main__":
    query_handler = QueryHandler(api_config_path="workflow/configs/api_config.json", db_config_path="workflow/configs/dbconfig.json")
    query_handler.handle_query("workflow/flight_queries/example.json")

