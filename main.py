import argparse

import urllib.parse
from typing import Optional, List

import requests

MUSICBRAINZ_URL = "https://musicbrainz.org/ws/2/"
MUSICBRAINZ_DEFAULT_PARAMETERS = {"fmt": "json"}
DEBUG_LOGGING = True


def lookup_artist_id(artist: str) -> Optional[str]:
    """ Find an artist ID from the name. """
    url = artist_lookup_url(artist)
    response = requests.get(url)
    artists = response.json().get("artists")

    if artists:
        artist = artists[0]

        if DEBUG_LOGGING:
            print(f"Picking the most relevant '{artist['type']}' with id '{artist['id']}', called "
                  f"'{artist['name']}', from '{artist['country']}', with confidence {artist['score']}%")

        # TODO: return the list and prompt the user to pick the right one. Maybe only if score < 100.
        return artist["id"]

    return None


def releases(artist_id: str, chunk_by: int = 100) -> List[str]:
    """ Find all releases by an artist. """
    releases_ids: List[str] = []
    while True:
        url = release_search_url(artist_id, limit=chunk_by)
        response = requests.get(url)
        current_releases = response.json().get("releases")
        if current_releases:
            releases_ids += [x["id"] for x in current_releases]
            if DEBUG_LOGGING:
                print(f"Fetched {len(current_releases)} releases.")

        if not current_releases or len(current_releases) < chunk_by:
            break

    if DEBUG_LOGGING:
        print(f"Finished fetching {len(releases_ids)} releases.")
    return releases_ids


def artist_lookup_url(artist: str) -> str:
    url = urllib.parse.urljoin(MUSICBRAINZ_URL, f"artist")
    query = urllib.parse.urlencode({"query": artist, **MUSICBRAINZ_DEFAULT_PARAMETERS})
    return f"{url}?{query}"


def release_search_url(artist_id: str, limit: int = None, offset: int = None) -> str:
    url = urllib.parse.urljoin(MUSICBRAINZ_URL, f"release")
    parameters = {"artist": artist_id}
    if limit is not None:
        parameters["limit"] = limit
    if offset is not None:
        parameters["offset"] = offset
    query = urllib.parse.urlencode({**parameters, **MUSICBRAINZ_DEFAULT_PARAMETERS})
    return f"{url}?{query}"


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
