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

    def test_as_array(self):
        a = random((3,))
        n = self.rb.nodes.create(*a)
        self.assertIsInstance(n, ar.nodes.ExtendedNode)
        assert_array_almost_equal(a, n.as_array())

    def test_dist_to(self):
        a = random((3,))
        b = random((3,))
        node = self.rb.nodes.create(*a)
        other = self.rb.nodes.create(*b)
        self.assertAlmostEqual(node.dist_to(other), np.linalg.norm(b - a))

    def test_closest(self):
        ns = [self.rb.nodes.create(*random((3,))) for i in range(10)]
        n = ns.pop()
        ns_sorted = [p.Number for p in sorted(ns, key=lambda p: n.dist_to(p))]
        self.assertSequenceEqual(n.closest('1to9', count=-1), ns_sorted)
        self.assertEqual(n.closest('1to9'), ns_sorted[0])
        self.assertEqual(n.closest('1to9', obj=True).Number, ns_sorted[0])
        self.assertSequenceEqual(n.closest('1to9', count=3), ns_sorted[:3])
        self.assertSequenceEqual(
            [p.Number for p in n.closest('1to9', count=3, obj=True)],
            ns_sorted[:3]
        )


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

    def test_server(self):
        self.assertIsInstance(
            self.rb.nodes,
            ar.nodes.ExtendedNodeServer
        )

    def test_create(self):
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

    def test_get(self):
        a = random((3,))
        n = self.rb.nodes.create(*a, num=4, obj=False)
        self.assertIsInstance(n, int)
        self.assertEqual(self.rb.nodes.get(n).Number, 4)
        assert_array_almost_equal(a, self.rb.nodes.get(n).as_array())

    def test_select(self):
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

    def test_delete(self):
        for i in range(1, 10):
            self.rb.nodes.create(*random((3,)))
        self.rb.nodes.delete('all')
        self.assertListEqual(list(self.rb.nodes.select('all')), [])

    def test_table(self):
        a = random((10, 3))
        for r in a:
            self.rb.nodes.create(*r)
        t = self.rb.nodes.table('2to8by3')
        # Indexing excludes last value in numpy and starts at 0, hence 1:8:3
        assert_array_almost_equal(t[:, 1:], a[1:8:3, :])
        assert_array_equal(t[:, :1].flatten(), np.array([2, 5, 8]))

    def test_from_array(self):
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

    def test_set_support(self):
        self.rb.supports.create('test_set', '111111')
        self.rb.nodes.set_support('all', 'test_set')
        for n in self.rb.nodes.select('all'):
            label = ar.RobotOM.IRobotLabel(
                n.GetLabel(ar.RobotOM.IRobotLabelType.I_LT_SUPPORT))
            self.assertEqual(label.Name, 'test_set')


if __name__ == '__main__':
    unittest.main()
