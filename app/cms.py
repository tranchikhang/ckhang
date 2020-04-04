import os
import json

def read_json_data():
    cwd = os.path.dirname(os.path.abspath(__file__))
    json_file = open(os.path.join(cwd, 'posts.json'), 'r')
    data = json.load(json_file)
    return data