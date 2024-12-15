import graphene
from graphene import ObjectType, List, String, Int, Float
import requests

# 19 columns
class GameDataType(graphene.ObjectType):
    app_id = Int()
    name = String()
    release_date = String()
    required_age = Int()
    price = Float()
    dlc_count = Int()
    about_the_game = String()
    supported_languages = String()
    windows = Int()
    mac = Int()
    linux = Int()
    positive = Int()
    negative = Int()
    score_rank = Float()
    developers = String()
    publishers = String()
    categories = String()
    genres = String()
    tags = String()

class Query(ObjectType):
    # Define the query for fetching game data with the 21 parameters (19 columns + 2 date filters)
    game_data = List(GameDataType,
                     app_id=Int(),
                     name=String(),
                     release_date=String(),
                     required_age=Int(),
                     price=Float(),
                     dlc_count=Int(),
                     about_the_game=String(),
                     supported_languages=String(),
                     windows=Int(),
                     mac=Int(),
                     linux=Int(),
                     positive=Int(),
                     negative=Int(),
                     score_rank=Float(),
                     developers=String(),
                     publishers=String(),
                     categories=String(),
                     genres=String(),
                     tags=String(),
                     release_date__gte=String(),
                     release_date__lte=String())

    def resolve_game_data(self, info, **params):
        """
        Dynamically handle the query and apply filtering based on input params.
        This will send the request to your /data_explorer endpoint with the given parameters.
        """
        # Build the query parameters for the /data_explorer API
        query_params = {}
        
        # Iterate through all parameters and add them to the query
        for key, value in params.items():
            if value is not None:
                query_params[key] = value
        
        # Make the request to the Flask API (/data_explorer)
        response = requests.get('http://127.0.0.1:5000/data_explorer', params=query_params)
        
        # If the response is successful, return the JSON data
        if response.status_code == 200:
            return response.json().get('data', [])
        else:
            return []

# Define the GraphQL schema
schema = graphene.Schema(query=Query)
