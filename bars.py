import json
import math
import sys


def load_data(file_name):
    try:
        with open(file_name, encoding='utf-8') as json_file:
            json_string = json_file.read()
            decoded_json = json.loads(json_string)
            return decoded_json['features']
    except (FileNotFoundError, ValueError):
        return None


def get_biggest_bar(list_of_bars):
    biggest_bar = max(
        list_of_bars,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return biggest_bar


def get_smallest_bar(list_of_bars):
    smallest_bar = min(
        list_of_bars,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return smallest_bar


def get_closest_bar(list_of_bars, my_longitude, my_latitude):
    my_latitude *= math.pi / 180
    my_longitude *= math.pi / 180
    closest_bar = min(
        list_of_bars,
        key=lambda index: calculate_distance(
            index['geometry']['coordinates'][0],
            index['geometry']['coordinates'][1]
        )
    )
    return closest_bar


def calculate_distance(bar_longitude, bar_latitude):
    earth_radius = 6371000
    bar_latitude *= math.pi / 180
    bar_longitude *= math.pi / 180
    distance = math.acos(
        math.sin(my_latitude)*math.sin(bar_latitude) +
        math.cos(my_latitude) * math.cos(bar_latitude) *
        math.cos(my_longitude-bar_longitude)
    )
    return distance*earth_radius


def get_bar_name(bar):
    bar_name = bar['properties']['Attributes']['Name']
    return bar_name


if __name__ == '__main__':
    if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
        print('Usage: {0} + your_file.json'.format(sys.argv[0]))
        sys.exit()
    list_of_bars = load_data(sys.argv[1])
    if list_of_bars is None:
        sys.exit('Error: file not found or no json object could be decoded')
    bar = get_biggest_bar(list_of_bars)
    print('The biggest bar:', get_bar_name(bar))
    bar = get_smallest_bar(list_of_bars)
    print('The smallest:', get_bar_name(bar))
    try:
        my_latitude = float(input('Input your current latitude:'))
        my_longitude = float(input('Input your current longitude:'))
        bar = get_closest_bar(list_of_bars, my_longitude, my_latitude)
        print('The closest bar:', get_bar_name(bar))
    except ValueError as err:
        print(err)
