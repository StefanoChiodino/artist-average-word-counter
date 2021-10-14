import unittest

from parameterized import parameterized

from src.api import Api


class ApiEndToEndTests(unittest.TestCase):
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


if __name__ == '__main__':
    unittest.main()
