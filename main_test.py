import unittest

from parameterized import parameterized

from main import word_count


class ArtistAverageWordCounterTest(unittest.TestCase):
    @parameterized.expand([
        ("Chissà, chissà chi sei", 4),
        ("Chissà , chissà chi sei", 4),
        ("a b c", 3),
        ("%$£%", 0),
        ("Inseguendo una libellula in un prato\r\nUn giorno che avevo rotto col passato\r\n"
         "Quando già credevo di esserci riuscito\r\nSon caduto", 21),
    ])
    def test_word_count(self, text, expected):
        average = word_count(text)
        self.assertEqual(average, expected)


if __name__ == '__main__':
    unittest.main()
