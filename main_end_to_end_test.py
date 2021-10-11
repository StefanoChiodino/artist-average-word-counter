import unittest

from main import musicbrainz_artist_id


class ArtistAverageWordCounterTest(unittest.TestCase):
    def test_musicbrainz_artist_id(self):
        artist_id = musicbrainz_artist_id("metallica")

        self.assertIsNotNone(artist_id)


if __name__ == '__main__':
    unittest.main()
