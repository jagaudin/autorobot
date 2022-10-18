import unittest
import time
from itertools import combinations
import numpy as np
from numpy.random import random
from numpy.testing import assert_array_equal

import autorobot as ar


class TestExtendedBar(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        time.sleep(2)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def tearDown(self):
        self.rb.structure.Clear()

    def test_properties(self):
        a1, a2 = random((3,)), random((3,))
        n1 = self.rb.nodes.create(*a1)
        n2 = self.rb.nodes.create(*a2)
        b = self.rb.bars.create(n1, n2)
        sect = self.rb.sections.load('UB 305x165x40')
        mat = self.rb.materials.load('STEEL')
        release = self.rb.releases.create('UX-UZ', '011111', '110111')
        self.rb.bars.set_section(b.Number, sect)
        self.rb.bars.set_material(b.Number, mat)
        self.rb.bars.set_release(b.Number, release)
        with self.subTest(msg='section getter'):
            self.assertEqual(b.section.Name, 'UB 305x165x40')
        with self.subTest(msg='material getter'):
            self.assertEqual(b.material.Name, 'STEEL')
        with self.subTest(msg='release getter'):
            self.assertEqual(b.release.Name, 'UX-UZ')

        sect = self.rb.sections.create('Rnd10', 10)
        mat = self.rb.materials.load('S355')
        release = self.rb.releases.create('UZ-UX', '110111', '011111')
        b.section = sect.Name
        b.material = mat.Name
        b.release = release.Name
        with self.subTest(msg='section setter'):
            self.assertEqual(b.section.Name, 'Rnd10')
        with self.subTest(msg='material setter'):
            self.assertEqual(b.material.Name, 'S355')
        with self.subTest(msg='release setter'):
            self.assertEqual(b.release.Name, 'UZ-UX')

        b.RemoveLabel(ar.RobotOM.IRobotLabelType.I_LT_BAR_SECTION)
        b.RemoveLabel(ar.RobotOM.IRobotLabelType.I_LT_BAR_MATERIAL)
        b.RemoveLabel(ar.RobotOM.IRobotLabelType.I_LT_BAR_RELEASE)
        with self.subTest(msg='section defaults to None'):
            self.assertEqual(b.section, None)
        with self.subTest(msg='material defaults to None'):
            self.assertEqual(b.material, None)
        with self.subTest(msg='release defaults to None'):
            self.assertEqual(b.release, None)


class TestBarServers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        time.sleep(2)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def tearDown(self):
        self.rb.structure.Clear()

    def test_server(self):
        self.assertIsInstance(
            self.rb.bars,
            ar.app.ExtendedBarServer
        )

    def test_create(self):
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

    def test_get(self):
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        b = self.rb.bars.create(n1, n2)
        self.assertEqual(self.rb.bars.get(b.Number).Number, b.Number)

    def test_select(self):
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

    def test_delete(self):
        ns = [self.rb.nodes.create(*random((3,))) for i in range(10)]
        with self.rb.bars as bars:
            for n1, n2 in combinations(ns, 2):
                bars.create(n1, n2)
        self.rb.bars.delete('all')
        self.assertListEqual(list(self.rb.bars.select('all')), [])

    def test_table(self):
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

    def test_set_section(self):
        self.rb.sections.create('Rnd10', 10)
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        b = self.rb.bars.create(n1, n2)
        self.rb.bars.set_section('all', 'Rnd10')
        for b in self.rb.bars.select('all'):
            label = ar.RobotOM.IRobotLabel(
                b.GetLabel(ar.RobotOM.IRobotLabelType.I_LT_BAR_SECTION))
            self.assertEqual(label.Name, 'Rnd10')

    def test_set_material(self):
        self.rb.materials.load('STEEL')
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        b = self.rb.bars.create(n1, n2)
        self.rb.bars.set_material('all', 'STEEL')
        for b in self.rb.bars.select('all'):
            label = ar.RobotOM.IRobotLabel(
                b.GetLabel(ar.RobotOM.IRobotLabelType.I_LT_MATERIAL))
            self.assertEqual(label.Name, 'STEEL')

    def test_set_release(self):
        self.rb.releases.create('UX-UZ', '011111', '110111')
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        b = self.rb.bars.create(n1, n2)
        self.rb.bars.set_release('all', 'UX-UZ')
        for b in self.rb.bars.select('all'):
            label = ar.RobotOM.IRobotLabel(
                b.GetLabel(ar.RobotOM.IRobotLabelType.I_LT_BAR_RELEASE))
            self.assertEqual(label.Name, 'UX-UZ')


if __name__ == '__main__':
    unittest.main()
