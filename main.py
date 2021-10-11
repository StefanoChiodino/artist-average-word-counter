import argparse

import urllib.parse
from typing import Optional, List, Generator, Iterable
from urllib import request

import musicbrainzngs
import requests as requests

DEBUG_LOGGING = True
LYRICS_API_BASE_URL = "https://api.lyrics.ovh/v1/"

musicbrainzngs.set_useragent("Artist Average Word Count", "0.1", "https://stefano.chiodino.uk")


def song_lyrics(artist: str, song: str) -> Optional[str]:
    """ Find the lyrics for a song. """
    url = urllib.parse.urljoin(LYRICS_API_BASE_URL, f"{artist}/{song}")
    response = requests.get(url)
    return response.json().get("lyrics")


def lookup_artist_id(artist: str) -> Optional[str]:
    """ Find an artist ID from the name. """
    response = musicbrainzngs.search_artists(artist)
    artists = response.get("artist-list")

    if artists:
        artist = artists[0]

        if DEBUG_LOGGING:
            print(f"Picking the most relevant '{artist['type']}' with id '{artist['id']}', called "
                  f"'{artist['name']}', from '{artist['country']}', with confidence {artist['ext:score']}%")

        # TODO: return the list and prompt the user to pick the right one. Maybe only if score < 100.
        return artist["id"]

    return None


def song_titles(artist_id: str, chunk_by: int = 100) -> Iterable[str]:
    """ All titles of songs by an artist. """
    current_offset = 0
    while True:
        response = musicbrainzngs.browse_works(artist=artist_id, limit=chunk_by, offset=current_offset)
        works = response.get("work-list")
        if not works:
            return
        songs = [x for x in works if x.get("type") == "Song"]
        if DEBUG_LOGGING:
            print(f"Finished fetching {len(songs)} songs, from {len(works)} works.")
        current_offset += chunk_by
        yield [x.get("title") for x in songs]

        if len(works) < chunk_by:
            return


def average_lyrics_words(artist: str):
    artist_id = lookup_artist_id(artist)
    pass


def main() -> None:
    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    arg_parser.add_argument("artist")

    args = arg_parser.parse_args()

    average_lyrics_words(args.artist)


if __name__ == "__main__":
    main()
