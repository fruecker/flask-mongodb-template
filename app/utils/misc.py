
import json
from random import randint

def get_random_from_list(array:list):
    if not array:
        return None
    return array[randint(0, len(array)-1)]


def find_next_lowest_number_in_list(array:list, start_value=1):
    number = start_value
    if not array:
        return number
    while number in array:
        number += 1
    return number


def update_response_data(response, **kwargs):
    data = response.get_json()
    data.update(**kwargs)
    response.data = json.dumps(data) 
    return response


def populate_obj(obj, skip_none=False, **kwargs):
    for attr in dir(obj):
        if attr in kwargs:
            # Skip if value is None and its not allowed
            if skip_none and (kwargs[attr] is None):
                continue
            setattr(obj, attr, kwargs[attr])