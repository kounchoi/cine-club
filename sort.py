#!/usr/bin/env python

"""Sort proposals by IMDb rating."""

import argparse
import json
from operator import itemgetter
from html.parser import HTMLParser
from urllib.request import urlopen

import yaml


class JSONExtractor(HTMLParser):
    """Extracts ld+json data."""

    def __init__(self):
        super().__init__()
        self.data = []
        self.in_ldjson = False


    def handle_data(self, data):
        if self.in_ldjson:
            self.data.append(data)
            self.in_ldjson = False


    def handle_starttag(self, tag, attributes):
        if tag != 'script':
            return

        for name, value in attributes:
            if name == 'type' and value == 'application/ld+json':
                self.in_ldjson = True
                return


def get_rating(imdb_id):
    """Find rating for given IMDb ID."""

    response = urlopen('https://www.imdb.com/title/' + imdb_id)
    parser = JSONExtractor()

    while True:
        line = response.readline()
        if not line:
            break
        parser.feed(line.decode('utf-8'))

    if len(parser.data) != 1:
        raise RuntimeError(
            'Expected to find exactly 1 ld+json entry '
            'but got {}.'.format(len(parser.data))
        )

    data = json.loads(parser.data[0])
    return float(data['aggregateRating']['ratingValue'])


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(__doc__)
    arg_parser.add_argument('list', help='YAML file with a list of movies.')
    args = arg_parser.parse_args()

    rated_movies = []

    with open(args.list) as f:
        for entry in yaml.safe_load(f):
            rated_movies.append((entry, get_rating(entry['imdb_id'])))

    rated_movies.sort(key=itemgetter(1), reverse=True)
    for entry in rated_movies:
        print(entry[1], entry[0]['imdb_id'], entry[0]['title'])

