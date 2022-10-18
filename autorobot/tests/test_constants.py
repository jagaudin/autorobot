import unittest
from random import randrange

import autorobot as ar


class TestEnumCapsule(unittest.TestCase):

    def test_member_type(self):
        for name in ar.constants.__all__:
            enum = getattr(ar.constants, name)
            with self.subTest(msg=f'{name} member type'):
                for v in enum.values():
                    self.assertTrue(isinstance(v, enum._inst))

    def test_contains_original_pairs(self):
        for name in ar.constants.__all__:
            enum = getattr(ar.constants, name)
            with self.subTest(msg=f'{name} original pairs'):
                for name in enum.GetNames(enum._inst):
                    self.assertIn(name, enum)

    def test_access_keys_as_attributes(self):
        for name in ar.constants.__all__:
            enum = getattr(ar.constants, name)
            with self.subTest(msg=f'{name} attributes'):
                for name in enum.keys():
                    self.assertTrue(hasattr(enum, name))

    def test_custom_index_keys(self):
        for name in ar.constants.__all__:
            enum = getattr(ar.constants, name)
            with self.subTest(msg=f'{name} custom_index'):
                self.assertEqual(
                    set(enum.custom_index.keys()),
                    set(enum.keys() - set(enum.GetNames(enum._inst)))
                )

    def test_iteration(self):
        for name in ar.constants.__all__:
            enum = getattr(ar.constants, name)
            with self.subTest(msg=f'{name} iteration'):
                self.assertEqual(
                    len(list(enum)),
                    len(set(int(i) for i in enum.values()))
                )
                self.assertEqual(
                    set(int(i) for i in enum),
                    set(int(i) for i in enum.values())
                )

    def test_is_callable(self):
        for name in ar.constants.__all__:
            enum = getattr(ar.constants, name)
            number = randrange(200)
            with self.subTest(msg=f'{name} is callable'):
                new_value = enum(number)
                self.assertTrue(isinstance(new_value, enum._inst))
                self.assertEqual(int(new_value), number)
            with self.subTest(msg=f'calling {name} with unchecked=False'):
                for value in enum:
                    self.assertEqual(
                        int(enum(int(value), unchecked=False)), int(value))
                max_value = max(int(value) for value in enum)
                with self.assertRaises(ValueError):
                    enum(max_value + 1, unchecked=False)
