import unittest
from unittest import mock
from unittest.mock import MagicMock

from src.artist_average_word_counter import Api


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

    @mock.patch("musicbrainzngs.search_artists")
    def test_lookup_artist_interactive_can_not_be_bamboozled(self, mock_search_artist: MagicMock):
        file_mock = MagicMock()
        input_mock = MagicMock()
        # A QA engineer walks into a bar...
        input_mock.side_effect = ["0", "99999999999", "lizard", "-1", "ueicbksjdhd", "1"]
        mock_search_artist.return_value = {"artist-list": [{"name": "name1", "id": "1"}]}

        response = self.api.lookup_artist_interactive("query", interactive=True, input_pipe=input_mock,
                                                      output_pipe=file_mock)

        self.assertIsNotNone(response)
        artist, artist_id = response
        self.assertEqual(artist, "name1")
        self.assertEqual(artist_id, "1")
        self.assertIn("Please enter a number", str(file_mock.write.call_args_list))
        self.assertIn("enter a positive number below", str(file_mock.write.call_args_list))


if __name__ == '__main__':
    unittest.main()
