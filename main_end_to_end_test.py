import unittest

from parameterized import parameterized

from main import lookup_artist_id, song_titles, song_lyrics


class ArtistAverageWordCounterTest(unittest.TestCase):
    @parameterized.expand([("Metallica", "65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab"),
                           ("metallica", "65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab"),
                           ("Lucio Battisti", "c0c0de23-d9c1-4776-97e0-0c2529402622"),
                           ("battisti", "c0c0de23-d9c1-4776-97e0-0c2529402622"),
                           ])
    def test_lookup_artist_id(self, artist: str, expected: str):
        artist_id = lookup_artist_id(artist)
        self.assertEqual(artist_id, expected)

    def test_song_titles(self):
        titles = song_titles("65f4f0c5-ef9e-490c-aee3-909e7ae6b2ab")
        self.assertGreater(len(list(titles)), 0)

    def test_song_lyrics(self):
        lyrics = song_lyrics("Lucio Battisti", "Con il nastro rosa")
        self.assertGreater(len(list(lyrics)), 0)
        self.assertIn("chissà chi sei", lyrics)


if __name__ == '__main__':
    unittest.main()
