import unittest
from numpy.random import random

import autorobot as ar


class TestExtendedRelease(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def test_properties(self):
        label = self.rb.releases.create('test_properties', '111000', '000111')
        with self.subTest(msg='start'):
            self.assertTrue(label.start.UX)
            self.assertTrue(label.start.UY)
            self.assertTrue(label.start.UZ)
            self.assertFalse(label.start.RX)
            self.assertFalse(label.start.RY)
            self.assertFalse(label.start.RZ)
        with self.subTest(msg='end'):
            self.assertFalse(label.end.UX)
            self.assertFalse(label.end.UY)
            self.assertFalse(label.end.UZ)
            self.assertTrue(label.end.RX)
            self.assertTrue(label.end.RY)
            self.assertTrue(label.end.RZ)


class TestExtendedReleaseServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)
        n1 = cls.rb.nodes.create(*random((3,)))
        n2 = cls.rb.nodes.create(*random((3,)))
        cls.b = cls.rb.bars.create(n1, n2)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def test_create(self):
        label = self.rb.releases.create('test_create', '001100', '110011')
        self.assertFalse(label.start.UX)
        self.assertFalse(label.start.UY)
        self.assertTrue(label.start.UZ)
        self.assertTrue(label.start.RX)
        self.assertFalse(label.start.RY)
        self.assertFalse(label.start.RZ)
        self.assertTrue(label.end.UX)
        self.assertTrue(label.end.UY)
        self.assertFalse(label.end.UZ)
        self.assertFalse(label.end.RX)
        self.assertTrue(label.end.RY)
        self.assertTrue(label.end.RZ)
        self.rb.releases.delete('test_create')

    def test_set(self):
        self.rb.releases.create('test_set', '000011', '110000')
        self.rb.releases.set(self.b.Number, 'test_set')
        self.assertEqual(self.b.release.Name, 'test_set')
        self.rb.releases.delete('test_set')

    def test_get(self):
        self.rb.releases.create('test_get', '100001', '010010')
        label = self.rb.releases.get('test_get')
        self.assertIsInstance(label, ar.releases.ExtendedReleaseLabel)
        self.assertEqual(label.Name, 'test_get')
        self.rb.releases.delete('test_get')

    def test_get_names(self):
        releases = self.rb.releases.get_names()
        self.assertGreater(len(releases), 0)
        new_release = 'test_get_names'
        self.rb.releases.create('test_get_names', '000111', '000111')
        releases.append(new_release)
        with self.subTest(msg='all'):
            names = self.rb.releases.get_names()
            self.assertSetEqual(set(names), set(releases))
        with self.subTest(msg='filter'):
            names = self.rb.releases.get_names(lambda s: False)
            self.assertEqual(len(names), 0)
        self.rb.releases.delete(new_release)

    def test_delete(self):
        self.rb.releases.create('test_delete', '001000', '000100')
        self.assertTrue(self.rb.releases.exist('test_delete'))
        self.rb.releases.delete('test_delete')
        self.assertFalse(self.rb.releases.exist('test_delete'))

    def test_exist(self):
        self.assertFalse(self.rb.releases.exist('test_exist'))
        self.rb.releases.create('test_exist', '010000', '000010')
        self.assertTrue(self.rb.releases.exist('test_exist'))
        self.rb.releases.delete('test_exist')
