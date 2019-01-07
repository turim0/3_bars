import json
import math


def load_data(file_path):
    with open(file_path) as json_file:
        json_string = json_file.read()
        parsed_string = json.loads(json_string)
    return parsed_string


def get_biggest_bar(data):
    biggest_bar = max(data['features'], key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return biggest_bar['properties']['Attributes']['Name']


def get_smallest_bar(data):
    smallest_bar = min(data['features'], key=lambda x: x['properties']['Attributes']['SeatsCount'])
    return smallest_bar['properties']['Attributes']['Name']


def get_closest_bar(data, my_longitude, my_latitude):
    my_latitude *= math.pi / 180
    my_longitude *= math.pi / 180

    def calculation(longitude, latitude):
        earth_radius = 6371000
        latitude *= math.pi / 180
        longitude *= math.pi / 180
        distance = math.acos(math.sin(my_latitude)*math.sin(latitude) +
                      math.cos(my_latitude)*math.cos(latitude)*math.cos(my_longitude-longitude))
        return distance*earth_radius
    closest_bar = min(data['features'], key=lambda index: calculation(
        index['geometry']['coordinates'][0],
        index['geometry']['coordinates'][1])
                      )
    return closest_bar['properties']['Attributes']['Name']


if __name__ == '__main__':
    print("Введите путь до файла: ")
    file_path = input()
    data = load_data(file_path)
    print('Самый большой бар:', get_biggest_bar(data))
    print('Самый маленький бар:', get_smallest_bar(data))
    latitude = float(input("Введите широту вашего текущего местоположения:"))
    longitude = float(input("Введите долготу вашего текущего местоположения:"))
    print('Ближайший бар:', get_closest_bar(data, longitude, latitude))
