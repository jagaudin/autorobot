import unittest

from random import randrange

import autorobot as ar


class test_colander_dict(unittest.TestCase):

    def test_default(self):
        number = randrange(200)
        d = ar.synonyms.ColanderDict({1: number})

        self.assertEqual(d[1], number)
        self.assertEqual(d[2], 2)
        o = object()
        self.assertIs(d[o], o)


class test_synonyms(unittest.TestCase):

    def test_dict(self):
        self.assertIsInstance(ar.synonyms.synonyms, ar.synonyms.ColanderDict)
        for key, value in ar.synonyms.synonyms.items():
            with self.subTest(msg=f'{str(key)}'):
                self.assertIsInstance(key, str)
