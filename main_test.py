import unittest

from parameterized import parameterized

from main import artist_lookup_url, release_search_url


class ArtistAverageWordCounterTest(unittest.TestCase):
    def test_artist_lookup_url(self):
        url = artist_lookup_url("metallica")
        self.assertEqual(url, "https://musicbrainz.org/ws/2/artist?query=metallica&fmt=json")

    @parameterized.expand([
        ("65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab", None, None,
         "https://musicbrainz.org/ws/2/release?artist=65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab&fmt=json"),
        ("65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab", 42, None,
         "https://musicbrainz.org/ws/2/release?artist=65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab&limit=42&fmt=json"),
        ("65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab", None, 42,
         "https://musicbrainz.org/ws/2/release?artist=65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab&offset=42&fmt=json"),
        ("65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab", 42, 666,
         "https://musicbrainz.org/ws/2/release?artist=65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab&limit=42&offset=666&fmt=json"),
    ])
    def test_release_search_url(self, artist_id: str, limit: int, offset: int, expected: str):
        url = release_search_url(artist_id, limit, offset)
        self.assertEqual(url, expected)


if __name__ == '__main__':
    unittest.main()
