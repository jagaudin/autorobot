import unittest
import time
from numpy.random import random

import autorobot as ar


class TestExtendedRelease(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        time.sleep(2)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def test_properties(self):
        label = self.rb.releases.create('test_properties', '111000', '000111')
        with self.subTest(msg='start'):
            self.assertTrue(int(label.start.UX))
            self.assertTrue(int(label.start.UY))
            self.assertTrue(int(label.start.UZ))
            self.assertFalse(int(label.start.RX))
            self.assertFalse(int(label.start.RY))
            self.assertFalse(int(label.start.RZ))
        with self.subTest(msg='end'):
            self.assertFalse(int(label.end.UX))
            self.assertFalse(int(label.end.UY))
            self.assertFalse(int(label.end.UZ))
            self.assertTrue(int(label.end.RX))
            self.assertTrue(int(label.end.RY))
            self.assertTrue(int(label.end.RZ))


class TestExtendedReleaseServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        time.sleep(2)
        cls.rb.new(ar.RProjType.SHELL)
        n1 = cls.rb.nodes.create(*random((3,)))
        n2 = cls.rb.nodes.create(*random((3,)))
        cls.b = cls.rb.bars.create(n1, n2)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def test_create(self):
        label = self.rb.releases.create('test_create', '001100', '110011')
        self.assertFalse(int(label.start.UX))
        self.assertFalse(int(label.start.UY))
        self.assertTrue(int(label.start.UZ))
        self.assertTrue(int(label.start.RX))
        self.assertFalse(int(label.start.RY))
        self.assertFalse(int(label.start.RZ))
        self.assertTrue(int(label.end.UX))
        self.assertTrue(int(label.end.UY))
        self.assertFalse(int(label.end.UZ))
        self.assertFalse(int(label.end.RX))
        self.assertTrue(int(label.end.RY))
        self.assertTrue(int(label.end.RZ))
        self.rb.releases.delete('test_create')

    def test_set(self):
        self.rb.releases.create('test_set', '000011', '110000')
        self.rb.releases.set('test_set', self.b.Number)
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
