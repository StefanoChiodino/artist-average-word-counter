import unittest
from unittest import mock
from unittest.mock import MagicMock


from src.api import Api


class ArtistAverageWordCounterTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = Api()

    @mock.patch("musicbrainzngs.search_artists")
    def test_lookup_non_existent_artist(self, mock_search_artist: MagicMock):
        mock_search_artist.return_value = {}
        response = self.api.lookup_artist("")
        self.assertIsNone(response)

    @mock.patch("musicbrainzngs.search_artists")
    def test_lookup_non_existent_artist(self, mock_search_artist: MagicMock):
        mock_search_artist.return_value = [
            {"name": "name1",
             "id":1,
             "country":"country1",
             "score": 100}
        ]
        response = self.api.lookup_artist_interactive("")
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
