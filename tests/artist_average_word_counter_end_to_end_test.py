import unittest
from unittest.mock import MagicMock

from parameterized import parameterized

from src.artist_average_word_counter import Api, run


class ArtistAverageWordCounterEndToEndTests(unittest.TestCase):
    def setUp(self) -> None:
        self.api = Api()

    @parameterized.expand([
        ("Metallica", "65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab", "Metallica"),
        ("metallica", "65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab", "Metallica"),
        ("Lucio Battisti", "c0c0de23-d9c1-4776-97e0-0c2529402622", "Lucio Battisti"),
        ("battisti", "c0c0de23-d9c1-4776-97e0-0c2529402622", "Lucio Battisti"),
    ])
    def test_lookup_artist(self, artist: str, expected_id: str, expected_name: str):
        actual_name, actual_id = self.api.lookup_artist(artist)
        self.assertEqual(actual_id, expected_id)
        self.assertEqual(actual_name, expected_name)

    def test_song_titles(self):
        titles = self.api.find_song_titles("65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab")
        self.assertGreater(len(list(titles)), 0)

    def test_song_lyrics(self):
        lyrics = self.api.find_song_lyrics("Lucio Battisti", "Con il nastro rosa")
        self.assertGreater(len(list(lyrics)), 0)
        self.assertIn("chissà chi sei", lyrics)

    def test_getting_average(self):
        file_mock = MagicMock()
        run(["Blind Faith"], file=file_mock)
        file_mock.write.assert_called()


if __name__ == '__main__':
    unittest.main()
