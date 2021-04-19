import json


def load_from_json(filename):
    with open(filename, 'r', encoding='utf-8') as infile:
        data = json.load(infile)
    return data


def save_to_json(data, filename):
    with open(filename, 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
