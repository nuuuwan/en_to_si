import os
import unittest
from functools import cache

from utils import File

from en_to_si import Transliterator


@cache
def get_test_data_list():
    lines = File(os.path.join('tests', 'TEST_DATA.txt')).read_lines()
    lines = [line.strip() for line in lines if not line.startswith('---')]
    n = len(lines)
    test_data_list = []
    for i in range(0, n, 2):
        pair = (lines[i], lines[i + 1])
        test_data_list.append(pair)
    return test_data_list


TEST_DATA_LIST = get_test_data_list()


class TestCase(unittest.TestCase):
    def test_si_to_en(self):
        t_si_to_en = Transliterator('si', 'en')
        for word_si, word_en in TEST_DATA_LIST:
            word_en_expected = t_si_to_en.transliterate(word_si)
            self.assertEqual(word_en_expected, word_en)

    def test_en_to_si(self):
        t_en_to_si = Transliterator('en', 'si')
        for word_si, word_en in TEST_DATA_LIST:
            word_si_expected = t_en_to_si.transliterate(word_en)
            self.assertEqual(word_si_expected, word_si)
