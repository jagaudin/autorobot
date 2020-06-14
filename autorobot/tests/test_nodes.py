import unittest
import numpy as np
from numpy.random import random
from numpy.testing import assert_array_equal, assert_array_almost_equal

import autorobot as ar


class TestExtendedNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def tearDown(self):
        self.rb.structure.Clear()

    def test_extended_node_as_array(self):
        a = random((3,))
        n = self.rb.nodes.create(*a)
        self.assertIsInstance(n, ar.nodes.ExtendedNode)
        assert_array_almost_equal(a, n.as_array())


class TestNodeServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def tearDown(self):
        self.rb.structure.Clear()

    def test_node_server(self):
        self.assertIsInstance(
            self.rb.nodes,
            ar.nodes.ExtendedNodeServer
        )

    def test_node_create(self):
        with self.subTest(msg='nodes.create'):
            a = random((3,))
            n = self.rb.nodes.create(*a)
            self.assertIsInstance(n, ar.nodes.ExtendedNode)
            assert_array_almost_equal(a, n.as_array())

        with self.subTest(msg='nodes.create (kwargs)'):
            a = random((3,))
            n = self.rb.nodes.create(*a, num=4, obj=False)
            self.assertIsInstance(n, int)
            self.assertEqual(self.rb.nodes.get(n).Number, 4)
            assert_array_almost_equal(a, self.rb.nodes.get(n).as_array())

        with self.subTest(msg='nodes.create (overwrite)'):
            a = random((3,))
            self.assertRaises(
                ar.errors.AutoRobotIdError,
                self.rb.nodes.create, *a, 4
            )
            n = self.rb.nodes.create(*a, num=4, overwrite=True)
            self.assertEqual(self.rb.nodes.get(n).Number, 4)
            assert_array_almost_equal(a, n.as_array())

    def test_node_get(self):
        a = random((3,))
        n = self.rb.nodes.create(*a, num=4, obj=False)
        self.assertIsInstance(n, int)
        self.assertEqual(self.rb.nodes.get(n).Number, 4)
        assert_array_almost_equal(a, self.rb.nodes.get(n).as_array())

    def test_node_select(self):
        for i in range(1, 20):
            self.rb.nodes.create(*random((3,)))
        with self.subTest(msg='nodes.select range'):
            self.assertListEqual(
                [n.Number for n in self.rb.nodes.select('4to16by4')],
                [4, 8, 12, 16]
            )
        with self.subTest(msg='nodes.select all'):
            self.assertEqual(
                len(list(self.rb.nodes.select('all'))),
                ar.RobotOM.IRobotCollection(self.rb.nodes.GetAll()).Count
            )

    def test_node_delete(self):
        for i in range(1, 10):
            self.rb.nodes.create(*random((3,)))
        self.rb.nodes.delete('all')
        self.assertListEqual(list(self.rb.nodes.select('all')), [])

    def test_node_table(self):
        a = random((10, 3))
        for r in a:
            self.rb.nodes.create(*r)
        t = self.rb.nodes.table('2to8by3')
        # Indexing excludes last value in numpy and starts at 0, hence 1:8:3
        assert_array_almost_equal(t[:, 1:], a[1:8:3, :])
        assert_array_equal(t[:, :1].flatten(), np.array([2, 5, 8]))

    def test_node_from_array(self):
        with self.subTest(msg='nodes.from_array 1d'):
            a = random((3,))
            n = self.rb.nodes.from_array(a)
            assert_array_almost_equal(a, n.as_array())

        with self.subTest(msg='nodes.from_array 2d 3cols'):
            a = random((10, 3))
            ns = self.rb.nodes.from_array(a)
            assert_array_almost_equal(a, np.stack([n.as_array() for n in ns]))

        with self.subTest(msg='nodes.from_array 2d 4cols'):
            a = random((10, 3))
            a = np.hstack([np.array([[i] for i in range(20, 30)]), a])
            ns = self.rb.nodes.from_array(a)
            assert_array_almost_equal(
                a[:, 1:], np.stack([n.as_array() for n in ns]))
            self.assertListEqual([n.Number for n in ns], list(range(20, 30)))


if __name__ == '__main__':
    unittest.main()