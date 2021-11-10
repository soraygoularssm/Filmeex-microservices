from .parser import parse_data
from .serializer import json_data , json_serializer

def retrive_data(target,callback , meta = None):

    if meta:
        json_el = json_data(url=target, callback=callback , meta = meta)
    else:
        json_el = json_data(url=target, callback=callback)

    response_el = parse_data(json_el)

    res_el = json_serializer(response_el)

    return res_el