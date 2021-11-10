from more_itertools import one
import json

def json_data(url, callback, spider="imdb", meta=None):
    data = {
        "request": {
        },
    }
    data['request']['url'] = url
    data['request']['callback'] = callback
    if meta:
        data['request']['meta'] = meta
    data['spider_name'] = spider

    data = json.dumps(data)

    return data

def json_serializer(response):
    r_text = json.loads(response.text)

    r_items = r_text.get('items')

    try:
        result = one(r_items)
    except:
        result = r_items

    return result