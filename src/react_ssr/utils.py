import json


def read_json(path_to_json):
    with open(path_to_json) as f:
        return json.loads(f.read())
