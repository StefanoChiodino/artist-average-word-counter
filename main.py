import argparse

import urllib.parse
from typing import Optional

import requests

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/"
MUSICBRAINZ_DEFAULT_PARAMETERS = {"fmt": "json"}
DEBUG_LOGGING = True


def musicbrainz_artist_id(artist: str) -> Optional[str]:
    url = artist_lookup_url(artist)
    response = requests.get(url)
    artists = response.json().get("artists")

    if artists:
        artist = artists[0]

        if DEBUG_LOGGING:
            print(f"Picking the most relevant '{artist['type']}' with id '{artist['id']}', called "
                  f"'{artist['name']}', from '{artist['country']}', with confidence {artist['score']}%")
        return artist["id"]

    return None


def artist_lookup_url(artist: str) -> str:
    url = urllib.parse.urljoin(MUSICBRAINZ_URL, f"artist")
    query = urllib.parse.urlencode({"query": artist, **MUSICBRAINZ_DEFAULT_PARAMETERS})
    return f"{url}?{query}"


def average_lyrics_words(artist: str):
    artist_id = musicbrainz_artist_id(artist)
    pass


def main() -> None:
    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    arg_parser.add_argument("artist")

    args = arg_parser.parse_args()

    average_lyrics_words(args.artist)


if __name__ == "__main__":
    main()
