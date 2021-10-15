#!/usr/bin/env python3

import argparse
import re
import sys
import urllib.parse
from statistics import mean
from typing import List, Tuple, TextIO, Optional, Callable, Iterable

import musicbrainzngs
import requests as requests

from tqdm import tqdm


def count_words(text: str) -> int:
    """ Count the words in a text."""
    # You have one problem. You choose to solve it with regex. You now have two problems.
    words = re.findall(r'\w+', text)
    return len(words)


class Api(object):
    LYRICS_API_BASE_URL = "https://api.lyrics.ovh/v1/"
    musicbrainzngs.set_useragent("Artist Average Word Count", "0.1", "https://stefano.chiodino.uk")

    def find_song_lyrics(self, artist: str, song: str) -> Optional[str]:
        """ Find the lyrics for a song. """
        url = urllib.parse.urljoin(self.LYRICS_API_BASE_URL, f"{artist}/{song}")
        response = requests.get(url)
        return response.json().get("lyrics")

    def lookup_artist(self, artist_query: str) -> Optional[Tuple[str, str]]:
        """ Find an artist name and ID from a query. """
        response = musicbrainzngs.search_artists(artist_query)
        artists = response.get("artist-list")

        if artists:
            artist = artists[0]
            return artist["name"], artist["id"]

        return None

    def lookup_artist_interactive(self, artist_query: str, interactive: bool = False,
                                  input_pipe: Callable[[], str] = input,
                                  output_pipe: TextIO = sys.stdout) -> Optional[Tuple[str, str]]:
        """ Find an artist name and ID from a query, prompting the user to pick one if necessary. """
        response = musicbrainzngs.search_artists(artist_query, limit=10)
        artists = response.get("artist-list")

        if not artists:
            print(f"Sorry, we couldn't find any artist with '{artist_query}'!", file=output_pipe)
            return None

        # I read this score comes straight from lucene, so it's a good use case for us.
        if not interactive and artists[0].get("ext:score") == "100":
            print(f"{artists[0]['name']}? We have found the perfect match!", file=output_pipe)
            return artists[0]["name"], artists[0]["id"]

        # Yes, I know, I thought there would have been a library for this too!
        choice: Optional[int] = None
        while not choice:
            print("Pick one of the following artists:", file=output_pipe)
            for i, artist in enumerate(artists, start=1):
                print(
                    f"{i}) {artist['name']} ({artist.get('type', 'unknown type of artist')}"
                    f" from {artist.get('country', 'unknown country')})'", file=output_pipe)
            try:
                choice = int(input_pipe())
            except ValueError:
                print("Please enter a number", file=output_pipe)
            else:
                if 0 < choice <= len(artists):
                    artist = artists[choice - 1]
                    print(f"You have picked {artist['name']}", file=output_pipe)
                    return artist["name"], artist["id"]
                else:
                    print(f"Please enter a positive number below {len(artists)}", file=output_pipe)
                    choice = None

    def find_song_titles(self, artist_id: str, chunk_by: int = 100) -> Iterable[str]:
        """ All titles of songs by an artist. """
        current_offset = 0
        while True:
            response = musicbrainzngs.browse_works(artist=artist_id, limit=chunk_by, offset=current_offset)
            works = response.get("work-list")
            if not works:
                return []
            songs = [x for x in works if x.get("type") == "Song"]
            current_offset += chunk_by
            for song in songs:
                yield song.get("title")

            if len(works) < chunk_by:
                return


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
