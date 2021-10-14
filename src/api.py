import sys
import urllib.parse
from typing import Optional, Tuple, Iterable, Callable, TextIO, Any

import musicbrainzngs
import requests as requests


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

    def lookup_artist_interactive(self, artist_query: str, interactive: bool, input_pipe: Callable[[], str] = input,
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
                print("Please enter a number")
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
                return
            songs = [x for x in works if x.get("type") == "Song"]
            current_offset += chunk_by
            for song in songs:
                yield song.get("title")

            if len(works) < chunk_by:
                return