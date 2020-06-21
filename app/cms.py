import os
import json
from paginate import Page


def read_json_data():
    cwd = os.path.dirname(os.path.abspath(__file__))
    json_file = open(os.path.join(cwd, 'posts.json'), 'r')
    data = json.load(json_file)
    data['posts'].reverse()
    return data['posts']


def get_post_in_page(data, page):
    current_page = Page(data, page=page, items_per_page=10)
    return current_page
