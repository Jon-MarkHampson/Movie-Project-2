import json

FILE_PATH = "movie_database.json"


def load_data():
    """ Loads a JSON file """
    with open(FILE_PATH, "r") as handle:
        return json.load(handle)['movies']


def save_data(data):
    """ Saves a JSON file """
    json_str = f'{{"movies": {json.dumps(data)}}}'
    with open(FILE_PATH, "w") as handle:
        handle.write(json_str)

load_data()