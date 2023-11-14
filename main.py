from workflow.query_handler import QueryHandler

if __name__ == "__main__":
    query_handler = QueryHandler("workflow/configs/api_config.json")
    query_handler.handle_query("workflow/flight_queries/example.json")
