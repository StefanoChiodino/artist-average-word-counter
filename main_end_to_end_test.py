import unittest

from main import lookup_artist_id, song_titles


class ArtistAverageWordCounterTest(unittest.TestCase):
    def test_lookup_artist_id(self):
        artist_id = lookup_artist_id("metallica")

        self.assertIsNotNone(artist_id)

    def test_song_titles(self):
        titles = song_titles("65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab")
        self.assertGreater(len(list(titles)), 0)


if __name__ == '__main__':
    unittest.main()
