# Artist Average Word Counter

Produce a program which, when given the name of an artist, will produce the average (mean) number of words in their songs.
This should be a CLI application that is usable from the command line.

# Requirements

Python 3.6+

# Run

Optionally, create a virtual environment with `python3 -m venv venv` and activate it with `source venv/bin/activate`.

Install dependencies with `pip3 install -r requirements.txt`

Run `python3 src/artist_average_word_counter.py "artist name"`.

Get help on the CLI with `python3 src/artist_average_word_counter.py --help`.

# Tests

Install dev dependencies with `pip3 install -r dev-requirements.txt`

Run `python3 -m unittest tests/*test.py`.

The tests in `artist_average_word_counter_end_to_end_test.py` uses live API.
