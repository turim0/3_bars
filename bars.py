#!/usr/bin/python3
# -*- coding: utf-8 -*-
import json
import math
import sys


def load_data():
    with open(sys.argv[1]) as json_file:
        json_string = json_file.read()
        parsed_string = json.loads(json_string)
        return parsed_string['features']


def get_biggest_bar_info(parsed_string):
    biggest_bar = max(parsed_string, key=lambda x:
                      x['properties']['Attributes']['SeatsCount'])
    return biggest_bar['properties']['Attributes']['Name']


def get_smallest_bar_info(parsed_string):
    smallest_bar = min(parsed_string, key=lambda x:
                       x['properties']['Attributes']['SeatsCount'])
    return smallest_bar['properties']['Attributes']['Name']


def get_closest_bar_info(parsed_string, my_longitude, my_latitude):
    my_latitude *= math.pi / 180
    my_longitude *= math.pi / 180
    closest_bar = min(parsed_string, key=lambda index: calculation(
                      index['geometry']['coordinates'][0],
                      index['geometry']['coordinates'][1]))
    return closest_bar['properties']['Attributes']['Name']


def calculation(bar_longitude, bar_latitude):
    earth_radius = 6371000
    bar_latitude *= math.pi / 180
    bar_longitude *= math.pi / 180
    distance = math.acos(math.sin(my_latitude)*math.sin(bar_latitude) +
                         math.cos(my_latitude) * math.cos(bar_latitude) *
                         math.cos(my_longitude-bar_longitude))
    return distance*earth_radius


if __name__ == '__main__':
    try:
        if len(sys.argv) == 1 or sys.argv[1] in {'-h', '--help'}:
            print('Usage: {0} + your_file.json'.format(sys.argv[0]))
            sys.exit()
        parsed_string = load_data()
        print('Самый большой бар:', get_biggest_bar_info(parsed_string))
        print('Самый маленький бар:', get_smallest_bar_info(parsed_string))
        my_latitude = float(input("Введите широту вашего текущего местоположения:"))
        my_longitude = float(input("Введите долготу вашего текущего местоположения:"))
        print('Ближайший бар:', get_closest_bar_info(parsed_string, my_longitude, my_latitude))
    except ValueError as err:
        print(err)
    except FileNotFoundError as err:
        print(err)
