#!/usr/bin/env python3

import argparse
import re
import sys
from statistics import mean
from typing import List, Tuple, TextIO

from tqdm import tqdm

from src.api import Api


def count_words(text: str) -> int:
    """ Count the words in a text, skipping punctuation."""
    # You have one problem. You choose to solve it with regex. You now have two problems.
    words = re.findall(r'\w+', text)
    return len(words)


def calculate_lyrics_stats(artist: str, api: Api, interactive: bool = True, silent: bool = False,
                           output_pipe: TextIO = sys.stdout) \
        -> Tuple[List[int], int]:
    """ Returns the word count of all lyrics found, and total number of songs. """
    response = api.lookup_artist_interactive(artist, interactive, output_pipe=output_pipe)
    if not response:
        return [], 0

    artist_name, artist_id = response

    word_counts: List[int] = []
    search_count = 0
    # Here would be relatively easy to parallelise with something like multiprocessing, but I fear it would be against
    # the APIs fair use policies.
    with tqdm(api.find_song_titles(artist_id), unit=" counts", disable=silent, file=output_pipe) as progress_bar:
        for song_title in progress_bar:
            lyrics = api.find_song_lyrics(artist_name, song_title)
            search_count += 1
            if lyrics:
                word_counts += [count_words(lyrics)]
            progress_bar.set_postfix(
                {"Average word count": mean(word_counts) if word_counts else 0,
                 "Lyrics found %": len(word_counts) / search_count})
            progress_bar.update()

    return word_counts, search_count


def run(args: List[str], api: Api = Api(), file=sys.stdout) -> None:
    """ Calculates and prints the average word count for an artist lyrics. """
    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    arg_parser.add_argument("-i", "--interactive", help="Always use interactive mode to pick the artist",
                            action='store_true')
    arg_parser.add_argument("artist")
    args = arg_parser.parse_args(args)

    word_counts, song_count = calculate_lyrics_stats(args.artist, api, args.interactive, output_pipe=file)

    lyrics_found_percent = len(word_counts) / song_count if song_count > 0 else 0
    print(f"Average word count: {mean(word_counts) if word_counts else 0}. "
          f"Lyrics found {len(word_counts)}/{song_count},` {lyrics_found_percent}%.", file=file)


def main() -> None:
    run(sys.argv[1:])


if __name__ == "__main__":
    main()
