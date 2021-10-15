# Artist Average Word Counter

Produce a program which, when given the name of an artist, will produce the average (mean) number of words in their songs.
This should be a CLI application that is usable from the command line.

# Requirements

Python 3.6+

# Set up

Optionally, create a virtual environment with `python3 -m venv venv` and activate it with `source venv/bin/activate`.

Install dependencies with `pip3 install -r requirements.txt`

# Run

Run `python3 src/artist_average_word_counter.py "artist name"`. You can add the `-i`/`--interactive` flag to force interactive mode to pick an artist instead of best match.

Get help on the CLI with `python3 src/artist_average_word_counter.py --help`.

# Tests

Install dev dependencies with `pip3 install -r dev-requirements.txt`

Run ` python -m unittest discover -s tests -p "*test.py"`.

Some tests use live API, and have been split into their own files.
