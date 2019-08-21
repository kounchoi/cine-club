# IIHE ciné club

This repository maintains a list of proposed movies for the IIHE ciné club and provides tools to choose from it.


## Database format

The list of all proposed movies is maintained in YAML file [`movies.yaml`](movies.yaml). The entry for a single movie is a mapping with the following keys:

* `title`: Movie's title, preferably in English.
* `imdb_id`: [IMDb](https://www.imdb.com/) ID matching pattern `tt\d+`.
* `proponent`: Name of the proponent of this movie.
* `date`: [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date when the movie was suggested.
* `description` (optional): Short description for the movie.
* `watched`: ISO 8601 date when the movie was watched. Added after the viewing.


## Selection

A random subset of movies that haven't been watched yet is constructed using script [`select.py`](select.py). It expects as an argument the [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601) date of foreseen screening. The date is used to seed the random number generator so that the results are reproducible. Here is an example command:

```sh
./select.py 2019-08-28
```


## Adding new proposals

To add new proposed movies to the database, send Andrey a link to an [IMDb](https://www.imdb.com/) entry and, optionally, a short (one or two sentences) description of the movie. This description will be circulated if the movie is selected. Alternatively, prepare a pull request with updates to [`movies.yaml`](movies.yaml), respecting the format described above.

If the movie is chosen for screening, it will be the responsibility of the movie's proponent to obtain it.