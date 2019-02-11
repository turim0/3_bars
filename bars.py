import json
import math
import sys


def load_data(file):
    try:
        with open(file) as json_file:
            json_string = json_file.read()
            parsed_dict = json.loads(json_string)
            return parsed_dict['features']
    except FileNotFoundError as err:
        print(err)
    except ValueError:
        print('No JSON object could be decoded')


def get_biggest_bar(parsed_string):
    biggest_bar = max(
        parsed_string,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return biggest_bar


def get_smallest_bar(parsed_string):
    smallest_bar = min(
        parsed_string,
        key=lambda x: x['properties']['Attributes']['SeatsCount']
    )
    return smallest_bar


def get_closest_bar(parsed_string, my_longitude, my_latitude):
    my_latitude *= math.pi / 180
    my_longitude *= math.pi / 180
    closest_bar = min(
        parsed_string,
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
    parsed_string = load_data(sys.argv[1])
    bar = get_biggest_bar(parsed_string)
    bar_name = get_bar_name(bar)
    print('Самый большой бар:', bar_name)
    bar = get_smallest_bar(parsed_string)
    bar_name = get_bar_name(bar)
    print('Самый маленький бар:', bar_name)
    try:
        my_latitude = float(input("Введите широту вашего текущего местоположения:"))
        my_longitude = float(input("Введите долготу вашего текущего местоположения:"))
        bar = get_closest_bar(parsed_string, my_longitude, my_latitude)
        bar_name = get_bar_name(bar)
        print('Ближайший бар:', get_bar_name(bar))
    except ValueError as err:
        print(err)
