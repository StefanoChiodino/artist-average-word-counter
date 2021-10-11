import unittest

from main import artist_lookup_url


class ArtistAverageWordCounterTest(unittest.TestCase):
    def test_artist_lookup_url(self):
        url = artist_lookup_url("metallica")

        self.assertEqual(url, "https://musicbrainz.org/ws/2/artist?query=metallica&fmt=json")


if __name__ == '__main__':
    unittest.main()
