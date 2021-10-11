import argparse
import re
import sys
import urllib.parse
from io import TextIOWrapper
from typing import Optional, Iterable, List, Tuple

import musicbrainzngs
import requests as requests
from tqdm import tqdm


class Api(object):
    LYRICS_API_BASE_URL = "https://api.lyrics.ovh/v1/"
    musicbrainzngs.set_useragent("Artist Average Word Count", "0.1", "https://stefano.chiodino.uk")

    def find_song_lyrics(self, artist: str, song: str) -> Optional[str]:
        """ Find the lyrics for a song. """
        url = urllib.parse.urljoin(self.LYRICS_API_BASE_URL, f"{artist}/{song}")
        response = requests.get(url)
        return response.json().get("lyrics")

    def lookup_artist(self, artist: str) -> Optional[Tuple[str, str]]:
        """ Find an artist name and ID from a query. """
        response = musicbrainzngs.search_artists(artist)
        artists = response.get("artist-list")

        if artists:
            artist = artists[0]
            # TODO: return the list and prompt the user to pick the right one. Maybe only if score < 100.
            # print(f"Picking the most relevant '{artist['type']}' with id '{artist['id']}', called "
            #          f"'{artist['name']}', from '{artist['country']}', with confidence {artist['ext:score']}%")
            return artist["name"], artist["id"]

        return None

    def find_song_titles(self, artist_id: str, chunk_by: int = 100) -> Iterable[str]:
        """ All titles of songs by an artist. """
        current_offset = 0
        while True:
            response = musicbrainzngs.browse_works(artist=artist_id, limit=chunk_by, offset=current_offset)
            works = response.get("work-list")
            if not works:
                return
            songs = [x for x in works if x.get("type") == "Song"]
            current_offset += chunk_by
            for title in [x.get("title") for x in songs]:
                yield title

            if len(works) < chunk_by:
                return


def count_words(text: str) -> int:
    """ Count the words in a text, skipping punctuation."""
    # You have one problem. You choose to solve it with regex. You now have two problems.
    words = re.findall(r'\w+', text)
    return len(words)


def calculate_lyrics_stats(artist: str, api: Api, silent: bool = False, file: TextIOWrapper = sys.stdout)\
        -> Tuple[List[int], int]:
    """ Returns the word count of all lyrics, and total songs. """
    response = api.lookup_artist(artist)
    if not response:
        return [], 0
    artist_name, artist_id = response
    word_counts: List[int] = []
    lyrics_found = 0
    search_count = 0
    # TODO: Parallelise? May go against API's fair usage policies.
    with tqdm(api.find_song_titles(artist_id), unit=" counts", disable=silent, file=file) as progress_bar:
        for song_title in progress_bar:
            lyrics = api.find_song_lyrics(artist_name, song_title)
            search_count += 1
            if lyrics:
                word_counts += [count_words(lyrics)]
                lyrics_found += 1
            progress_bar.set_postfix(
                {"Average word count": sum(word_counts) / lyrics_found if lyrics_found else 0,
                 "Lyrics found %": len(word_counts) / search_count})
            progress_bar.update()

    return word_counts, search_count


def main(args: List[str], file=sys.stdout) -> None:
    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    arg_parser.add_argument("artist")

    args = arg_parser.parse_args(args)

    word_counts, song_count = calculate_lyrics_stats(args.artist, Api(), file=file)

    print(f"Average word count: {sum(word_counts) / len(word_counts)}. Lyrics found {len(word_counts)}/{song_count},"
          f" {len(word_counts) / song_count}%.", file=file)


if __name__ == "__main__":
    main(sys.argv[1:])
