# Artist Average Word Counter

Produce a program which, when given the name of an artist, will produce the average (mean) number of words in their songs.
This should be a CLI application that is usable from the command line.

# Requirements

Python 3.6+

# Install

You can install this locally with `pip3 install --editable .`

You can install from github with `pip3 install git+https://github.com/StefanoChiodino/artist-average-word-counter`

# Run

Run `artist-average-word-counter artist name`.

Get help on the CLI with `artist-average-word-counter --help`.

# Tests

Install dependencies with `pip3 install -r dev-requirements.txt`

Run `python3 -m unittest tests/*`.

The tests in `artist_average_word_counter_end_to_end_test.py` use live API.
