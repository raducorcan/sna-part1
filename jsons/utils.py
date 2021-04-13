import json


def load_from_json(filename):
    with open(filename, 'r') as infile:
        data = json.load(infile)
    return data


def save_to_json(data, filename):
    with open(filename, 'w') as outfile:
        json.dump(data, outfile)
