import unittest
from typing import List
from unittest.mock import MagicMock

from parameterized import parameterized

from src.artist_average_word_counter import count_words, calculate_lyrics_stats, run


class ArtistAverageWordCounterTests(unittest.TestCase):
    @parameterized.expand([
        # I'm trying italian lyrics to make sure it works with more than just english characters.
        ("Chissà, chissà chi sei", 4),
        ("Chissà , chissà chi sei", 4),
        ("a b c", 3),
        ("%$ £%", 0),
        ("Inseguendo una libellula in un prato\r\nUn giorno che avevo rotto col passato\r\n"
         "Quando già credevo di esserci riuscito\r\nSon caduto", 21),
    ])
    def test_count_words(self, text, expected):
        average = count_words(text)
        self.assertEqual(average, expected)

    @parameterized.expand([
        ([], []),
        (["a b c", "a b"], [3, 2]),
        (["a b c", "a b", None], [3, 2]),
        (["Inseguendo una libellula in un prato\r\nUn giorno che avevo rotto col passato\r\n",
          "Chissà , chissà chi sei"], [13, 4]),
    ])
    def test_calculate_lyrics_stats(self, song_words: List[str], expected_word_counts):
        mock_api = MagicMock()
        mock_api.lookup_artist_interactive.return_value = ("artist", "artist_id")
        mock_api.find_song_lyrics.side_effect = song_words
        mock_api.find_song_titles.return_value = [str(i) for i in range(len(song_words))]

        word_counts, song_count = calculate_lyrics_stats("artist", mock_api, silent=True)

        self.assertEqual(word_counts, expected_word_counts)
        self.assertEqual(song_count, len(song_words))

    def test_getting_average_for_non_existing_artist(self):
        mock_api = MagicMock()
        mock_api.lookup_artist_interactive.return_value = ("artist", "artist_id")
        mock_api.find_song_lyrics.side_effect = []
        mock_api.find_song_titles.return_value = []
        file_mock = MagicMock()
        run(["Blind Faith"], file=file_mock, api=mock_api)


if __name__ == '__main__':
    unittest.main()
