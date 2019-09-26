#!/usr/bin/env python

"""Randomly select a given number of movies from proposals."""

import argparse
from operator import itemgetter
import random
import re

import yaml


if __name__ == '__main__':

    arg_parser = argparse.ArgumentParser(description=__doc__)
    arg_parser.add_argument('date', help='Viewing date in ISO 8601.')
    arg_parser.add_argument(
        '-d', '--database', default='movies.yaml',
        help='Database of proposed movies.')
    arg_parser.add_argument(
        '-n', '--number', type=int, default=3,
        help='Number of movies to select.')
    arg_parser.add_argument(
        '-e', '--exclude', action='append', default=[],
        help='Exclude proposals from these people.'
    )
    args = arg_parser.parse_args()
    args.exclude = set(args.exclude)

    if not re.match(r'^\d{4}-\d{2}-\d{2}$', args.date):
        raise RuntimeError(
            'Date "{}" does not match pattern YYYY-MM-DD.'.format(args.date))
    random.seed(args.date, version=2)

    with open(args.database) as f:
        proposals = [
            movie for movie in yaml.safe_load(f)
            if ('watched' not in movie
                and movie['proponent'] not in args.exclude)
        ]


    if len(proposals) <= args.number:
        print('Only', len(proposals),
              'proposals are available. Will not perform random sampling.')
        selected_movies = proposals
    else:
        selected_movies = random.sample(proposals, args.number)


    print('Selected movies:')
    for movie in sorted(selected_movies, key=itemgetter('title')):
        print()
        print(movie['title'])
        print(movie['imdb_id'])

        description = movie.get('description', None)
        if description:
            print(description)
