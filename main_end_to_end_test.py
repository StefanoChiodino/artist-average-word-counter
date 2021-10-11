import unittest

from main import lookup_artist_id, releases


class ArtistAverageWordCounterTest(unittest.TestCase):
    def test_lookup_artist_id(self):
        artist_id = lookup_artist_id("metallica")

        self.assertIsNotNone(artist_id)

    def test_releases(self):
        artist_id = releases("65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab")

        self.assertIsNotNone(artist_id)


if __name__ == '__main__':
    unittest.main()
