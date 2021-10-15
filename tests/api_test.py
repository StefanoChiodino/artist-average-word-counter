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
    def test_lookup_artist_interactive(self, mock_search_artist: MagicMock):
        file_mock = MagicMock()
        mock_search_artist.return_value = {"artist-list": [{"name": f"name{i}", "id": str(i)} for i in range(1, 4)]}

        response = self.api.lookup_artist_interactive("query", input_pipe=lambda: "2", output_pipe=file_mock)

        self.assertIsNotNone(response)
        artist, artist_id = response
        self.assertEqual(artist, "name2")
        self.assertEqual(artist_id, "2")

    @mock.patch("musicbrainzngs.search_artists")
    def test_lookup_artist_interactive_perfect_score(self, mock_search_artist: MagicMock):
        file_mock = MagicMock()
        mock_search_artist.return_value = {
            "artist-list": [{"name": f"name{i}", "id": str(i), "ext:score": "100"} for i in range(1, 4)]}

        response = self.api.lookup_artist_interactive("query", output_pipe=file_mock)

        self.assertIsNotNone(response)
        artist, artist_id = response
        self.assertEqual(artist, "name1")
        self.assertEqual(artist_id, "1")

    @mock.patch("musicbrainzngs.search_artists")
    def test_lookup_artist_interactive_perfect_score_force_interactive(self, mock_search_artist: MagicMock):
        file_mock = MagicMock()
        mock_search_artist.return_value = {
            "artist-list": [{"name": f"name{i}", "id": str(i), "ext:score": "100"} for i in range(1, 4)]}

        response = self.api.lookup_artist_interactive("query", interactive=True, input_pipe=lambda: "2",
                                                      output_pipe=file_mock)

        self.assertIsNotNone(response)
        artist, artist_id = response
        self.assertEqual(artist, "name2")
        self.assertEqual(artist_id, "2")

    @mock.patch("musicbrainzngs.search_artists")
    def test_lookup_artist_interactive_no_results(self, mock_search_artist: MagicMock):
        file_mock = MagicMock()
        mock_search_artist.return_value = {"artist-list": []}
        response = self.api.lookup_artist_interactive("query", output_pipe=file_mock)
        self.assertIsNone(response)


if __name__ == '__main__':
    unittest.main()
