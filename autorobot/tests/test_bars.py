import unittest
from itertools import combinations
import numpy as np
from numpy.random import random
from numpy.testing import assert_array_equal

import autorobot as ar


class TestBarServers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def tearDown(self):
        self.rb.structure.Clear()

    def test_bar_server(self):
        self.assertIsInstance(
            self.rb.bars,
            ar.app.ExtendedBarServer
        )

    def test_bar_create(self):
        with self.subTest(msg='bars.create (ExtendedNode)'):
            a1, a2 = random((3,)), random((3,))
            n1 = self.rb.nodes.create(*a1)
            n2 = self.rb.nodes.create(*a2)
            self.assertIsInstance(n1, ar.nodes.ExtendedNode)
            self.assertIsInstance(n2, ar.nodes.ExtendedNode)
            b = self.rb.bars.create(n1, n2)
            self.assertEqual(b.StartNode, n1.Number)
            self.assertEqual(b.EndNode, n2.Number)
            self.assertAlmostEqual(b.Length, np.sqrt(np.sum((a1 - a2) ** 2)))

        with self.subTest(msg='bars.create (IRobotNode)'):
            a1, a2 = random((3,)), random((3,))
            n1 = self.rb.nodes.create(*a1)
            n2 = self.rb.nodes.create(*a2)
            self.assertIsInstance(n1.node, ar.RobotOM.IRobotNode)
            self.assertIsInstance(n2.node, ar.RobotOM.IRobotNode)
            b = self.rb.bars.create(n1.node, n2.node)
            self.assertEqual(b.StartNode, n1.Number)
            self.assertEqual(b.EndNode, n2.Number)
            self.assertAlmostEqual(b.Length, np.sqrt(np.sum((a1 - a2) ** 2)))

        with self.subTest(msg='bars.create (int)'):
            a1, a2 = random((3,)), random((3,))
            n1 = self.rb.nodes.create(*a1, obj=False)
            n2 = self.rb.nodes.create(*a2, obj=False)
            self.assertIsInstance(n1, int)
            self.assertIsInstance(n2, int)
            b = self.rb.bars.create(n1, n2)
            self.assertEqual(b.StartNode, n1)
            self.assertEqual(b.EndNode, n2)
            self.assertAlmostEqual(b.Length, np.sqrt(np.sum((a1 - a2) ** 2)))

        with self.subTest(msg='overwrite'):
            a1, a2 = random((3,)), random((3,))
            n = self.rb.nodes.create(*a1, obj=False)
            self.assertRaises(
                ar.errors.AutoRobotIdError,
                self.rb.nodes.create, *a2, num=n, overwrite=False
            )
            n = self.rb.nodes.create(*a2, num=n, overwrite=True)
            a = n.as_array()
            for i in range(len(a)):
                self.assertAlmostEqual(a[i], a2[i])

    def test_bar_get(self):
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        b = self.rb.bars.create(n1, n2)
        self.assertEqual(self.rb.bars.get(b.Number).Number, b.Number)

    def test_bar_select(self):
        ns = [self.rb.nodes.create(*random((3,))) for i in range(10)]
        with self.rb.bars as bars:
            for n1, n2 in combinations(ns, 2):
                bars.create(n1, n2)
        self.assertEqual(
            ar.RobotOM.IRobotCollection(self.rb.bars.GetAll()).Count,
            45
        )
        with self.subTest(msg='bars.select range'):
            self.assertListEqual(
                [b.Number for b in self.rb.bars.select('2to8by2')],
                [2, 4, 6, 8]
            )
        with self.subTest(msg='bars.select all'):
            self.assertEqual(
                len(list(self.rb.bars.select('all'))),
                ar.RobotOM.IRobotCollection(self.rb.bars.GetAll()).Count
            )

    def test_bar_delete(self):
        ns = [self.rb.nodes.create(*random((3,))) for i in range(10)]
        with self.rb.bars as bars:
            for n1, n2 in combinations(ns, 2):
                bars.create(n1, n2)
        self.rb.bars.delete('all')
        self.assertListEqual(list(self.rb.bars.select('all')), [])

    def test_bar_table(self):
        ns = [
            self.rb.nodes.create(*random((3,)), obj=False) for i in range(10)
        ]
        with self.rb.bars as bars:
            for n1, n2 in combinations(ns, 2):
                bars.create(n1, n2)
        t = self.rb.bars.table('all')
        a = np.stack([np.array([i + 1, *t])
                     for i, t in enumerate(combinations(ns, 2))])
        assert_array_equal(t, a.astype(int))


if __name__ == '__main__':
    unittest.main()
