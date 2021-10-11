import argparse
import re
import sys
import urllib.parse
from pprint import PrettyPrinter
from typing import Optional, Iterable, List

import musicbrainzngs
import requests as requests
from tqdm import tqdm, gui

LYRICS_API_BASE_URL = "https://api.lyrics.ovh/v1/"

musicbrainzngs.set_useragent("Artist Average Word Count", "0.1", "https://stefano.chiodino.uk")


def find_song_lyrics(artist: str, song: str) -> Optional[str]:
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
        # TODO: return the list and prompt the user to pick the right one. Maybe only if score < 100.
        # print(f"Picking the most relevant '{artist['type']}' with id '{artist['id']}', called "
        #          f"'{artist['name']}', from '{artist['country']}', with confidence {artist['ext:score']}%")
        return artist["id"]

    return None


def find_song_titles(artist_id: str, chunk_by: int = 100) -> Iterable[str]:
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


def average_lyrics_words(artist: str):
    artist_id = lookup_artist_id(artist)
    word_counts: List[int] = []
    sample_size = 0
    # TODO: Parallelise? May go against their fair usage policies.
    with tqdm(find_song_titles(artist_id), unit=" counts", dynamic_ncols=True, file=sys.stderr) as progress_bar:
        for song_title in progress_bar:
            lyrics = find_song_lyrics(artist, song_title)
            if lyrics:
                word_counts += [count_words(lyrics)]
                sample_size += 1
                progress_bar.set_postfix({"Average word count": sum(word_counts) / sample_size})
                progress_bar.update()

    print(f"Average word count: {sum(word_counts) / sample_size}")


def main() -> None:
    arg_parser: argparse.ArgumentParser = argparse.ArgumentParser()
    arg_parser.add_argument("artist")

    args = arg_parser.parse_args()

    average_lyrics_words(args.artist)


if __name__ == "__main__":
    main()
