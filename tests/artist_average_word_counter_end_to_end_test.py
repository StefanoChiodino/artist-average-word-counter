import unittest
from unittest.mock import MagicMock

from parameterized import parameterized

from src.artist_average_word_counter import run


class ArtistAverageWordCounterEndToEndTests(unittest.TestCase):
    def test_getting_average(self):
        file_mock = MagicMock()
        run(["Blind Faith"], file=file_mock)
        file_mock.write.assert_called()


if __name__ == '__main__':
    unittest.main()
