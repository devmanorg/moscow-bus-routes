# Moscow Bus Routes Fetcher

This script allows you to get information about the routes of buses in Moscow, using data from the site  [http://www.maxikarta.ru/msk/transport](http://www.maxikarta.ru/msk/transport).
The obtained information about routes is saved to JSON files (a separate file is created for each route).

## How to install

For script to work, you need to install **Python 3.6+** and then install all dependencies:

```bash

$ pip install -r requirements.txt

```

## How to set up

```bash

$ python routes_fetcher.py -h
usage: routes_fetcher.py [-h] [--output OUTPUT] [--sleep SLEEP]

optional arguments:
  -h, --help       show this help message and exit
  --output OUTPUT  a base path for save info about routes (Default:
                   routes_info)
  --sleep SLEEP    timeout between requests of info about routes (secs,
                   default: 1s)

```

## How to launch

```bash

$ python routes_fetcher.py

```

## Output file format description

Information about each route is saved to a JSON file which has following format:

```json

{
    "name": "123",
    "station_start_name": "Station start name",
    "station_stop_name": "Station stop name",
    "coordinates": [
        [55.737738216989, 37.766498603829],
        [55.737804102698, 37.767100181882],
        [55.738144099218, 37.770198716798],
        [55.7373712545, 37.767387939018],
        [55.737738216989, 37.766498603829]
    ],
    "stations": [
        [
            ["55.7377382169892", "37.7664986038286"], "Station 1"
        ],
        [
            ["55.7387231051935", "37.7699326687046"], "Station 2"
        ],
        [
            ["55.7424470372339", "37.7674587488251"], "Station 3"
        ]
    ]
}

```

Where:

* **name** - route name (or number)
* **station_start_name**, **station_stop_name** - names of endpoint stations
* **coordinates** - a list of geographic coordinates in a format **(latitude, longitude)** describing the reference points of the sequential movement along the route.
* **stations** - a list of stations in the format **(coordinates, station_name)** through which the route passes
