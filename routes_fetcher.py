import argparse
import sys
import os
import json
import time
from collections import deque

import requests


ROUTE_TYPES = {
    1: 'bus',
    2: 'trolleybus',
    3: 'minibus_taxi',
    10: 'tram',
}

FETCHED_ROUTE_TYPES = {1}


def fetch_json_content(url, params=None):
    headers = {
        'Accept': 'application/json',
    }
    try:
        response = requests.get(url, params=params, headers=headers)
        return response.json() if response.ok else None
    except requests.exceptions.ConnectionError:
        return None


def fetch_route_geometry_info(route_id):
    params = {
        'route_id': route_id,
    }
    return fetch_json_content(
        url='http://www.maxikarta.ru/msk/transport/query/route-geom',
        params=params,
    )


def fetch_route_stations_info(route_id):
    params = {
        'route_id': route_id,
    }
    return fetch_json_content(
        url='http://www.maxikarta.ru/msk/transport/query/stations',
        params=params,
    )


def get_route_stations_essential_info(route_stations_info):
    route_stations_essential_info = [
        ((station['lat'], station['lon']), station['name'])
        for station in route_stations_info
    ]
    return get_list_without_adjacent_identical_items(route_stations_essential_info)


def get_list_without_adjacent_identical_items(source_list):
    output_list = []

    for item in source_list:
        if len(output_list) == 0:
            output_list.append(item)
            continue

        if item == output_list[-1]:
            continue

        output_list.append(item)

    return output_list


def get_ordered_route_segments(source_route_segments):
    segments_deque = deque(source_route_segments)

    list_of_continuous_segments = []

    while segments_deque:
        continuous_segments = []

        start_segment = segments_deque.popleft()

        continuous_segments.append(start_segment)

        for current_segment in continuous_segments:
            next_segments = list(
                filter(
                    lambda segment: current_segment[0] == segment[-1],
                    segments_deque,
                ),
            )
            if next_segments:
                next_segment = next_segments[0]
                continuous_segments.append(next_segment)
                segments_deque.remove(next_segment)

        list_of_continuous_segments.append(continuous_segments)

    return [segment for segments in list_of_continuous_segments for segment in segments]


def get_ordered_coordinates_for_closed_route(source_route_segments):
    ordered_route_coordinates = []

    ordered_route_segments = get_ordered_route_segments(source_route_segments)

    for route_segment in ordered_route_segments:
        ordered_route_segment_coordinates = [
            (latitude, longitude) for longitude, latitude in reversed(route_segment)
        ]
        ordered_route_coordinates.extend(ordered_route_segment_coordinates)

    ordered_route_coordinates.reverse()

    route_begin_coordinates = ordered_route_coordinates[0]
    ordered_route_coordinates.append(route_begin_coordinates)

    return get_list_without_adjacent_identical_items(ordered_route_coordinates)


def get_processed_route_info(
        route_info, route_coordinates_info, route_stations_info):
    ordered_route_coordinates = get_ordered_coordinates_for_closed_route(
        source_route_segments=route_coordinates_info,
    )
    route_stations_essential_info = get_route_stations_essential_info(
        route_stations_info=route_stations_info,
    )
    return {
        'name': route_info['name'],
        'station_start_name': route_info['station_start_name'],
        'station_stop_name': route_info['station_stop_name'],
        'coordinates': ordered_route_coordinates,
        'stations': route_stations_essential_info,
    }


def save_route_info(route_info, output_filepath):
    with open(output_filepath, 'w') as file_object:
        json.dump(route_info, file_object)


def get_command_line_arguments():
    parser = argparse.ArgumentParser()

    parser.add_argument(
        '--output',
        help='a base path for save info about routes (Default: routes_info)',
        default='routes_info',
        type=str,
    )
    parser.add_argument(
        '--sleep',
        help='timeout between requests of info about routes (secs, default: 1s)',
        default=1,
        type=int,
    )
    command_line_arguments = parser.parse_args()

    return command_line_arguments


def main():
    command_line_arguments = get_command_line_arguments()

    base_output_path = command_line_arguments.output
    timeout_between_requests = command_line_arguments.sleep

    routes_info = fetch_json_content(
        url='http://www.maxikarta.ru/msk/transport/query/routes',
    )

    if routes_info is None:
        sys.exit('Could not get info about routes. Check your internet connection')

    if not os.path.exists(base_output_path):
        os.makedirs(base_output_path, exist_ok=True)

    for route_info in routes_info['routes']:
        route_id = route_info['route_id']
        route_type_id = route_info['type']
        route_type = ROUTE_TYPES[route_type_id]
        route_name = route_info['name']

        if route_type_id not in FETCHED_ROUTE_TYPES:
            continue

        route_info_output_path = os.path.join(base_output_path, route_type)

        if not os.path.exists(route_info_output_path):
            os.mkdir(route_info_output_path)

        route_info_output_filepath = os.path.join(
            route_info_output_path,
            f'{route_name}.json',
        )
        if os.path.exists(route_info_output_filepath):
            continue

        print(f'Fetching info about {route_type} route #{route_name}...')

        route_geometry_info = fetch_route_geometry_info(route_id=route_id)
        route_stations_info = fetch_route_stations_info(route_id=route_id)

        output_route_info = get_processed_route_info(
            route_info=route_info,
            route_coordinates_info=route_geometry_info['geom']['coordinates'],
            route_stations_info=route_stations_info['stations'],
        )
        save_route_info(
            route_info=output_route_info,
            output_filepath=route_info_output_filepath,
        )
        time.sleep(timeout_between_requests)


if __name__ == '__main__':
    main()
