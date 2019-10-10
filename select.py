#!/usr/bin/env python

"""Randomly select a given number of movies from proposals."""

import argparse
import datetime
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
        '-v', '--votes', default='votes.yaml',
        help='Database of movies that have been put for voting.')
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

    if args.votes:
        with open(args.votes) as f:
            voted_movies = yaml.safe_load(f)
    else:
        voted_movies = {}


    if len(proposals) <= args.number:
        print('Only', len(proposals),
              'proposals are available. Will not perform random sampling.')
        selected_movies = proposals
    else:
        weights = [
            0.5 ** len(voted_movies.get(movie['imdb_id'], []))
            for movie in proposals
        ]
        selected_movies = []
        while len(selected_movies) < args.number:
            movie = random.choices(proposals, weights)[0]
            if all(m['imdb_id'] != movie['imdb_id'] for m in selected_movies):
                selected_movies.append(movie)


    print('Selected movies:')
    for movie in sorted(selected_movies, key=itemgetter('title')):
        print()
        print(movie['title'])
        print(movie['imdb_id'])

        description = movie.get('description', None)
        if description:
            print(description)


    # Update the file with movies proposed for voting
    if args.votes:
        date_tuple = tuple(int(t) for t in args.date.split('-'))

        for movie in selected_movies:
            imdb_id = movie['imdb_id']

            # Construct a new date object for each movie in order to
            # avoid writing anchors in YAML
            screening_date = datetime.date(*date_tuple)

            if imdb_id in voted_movies:
                dates = voted_movies[imdb_id]
                if screening_date not in dates:
                    dates.append(screening_date)
            else:
                voted_movies[imdb_id] = [screening_date]

        with open(args.votes, 'w') as f:
            yaml.safe_dump(voted_movies, f, default_flow_style=False)
