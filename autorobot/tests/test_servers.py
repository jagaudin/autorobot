import unittest
from itertools import combinations
import numpy as np
from numpy.random import random
from numpy.testing import assert_array_equal, assert_array_almost_equal

import autorobot as ar


class TestDataServers(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def tearDown(self):
        self.rb.structure.Clear()

    # Bar server test

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

    # Case server test

    def test_case_server(self):
        self.assertIsInstance(
            self.rb.cases,
            ar.app.ExtendedCaseServer
        )

    def test_create_load_case(self):
        with self.subTest(msg='cases.create_load_case'):
            c = self.rb.cases.create_load_case(1, 'Dummy', ar.RCaseNature.PERM,
                                               ar.RAnalysisType.LINEAR)
            self.assertEqual(c.Name, 'Dummy')

        with self.subTest(msg='cases.create_load_case (overwrite)'):
            self.assertRaises(
                ar.errors.AutoRobotIdError,
                self.rb.cases.create_load_case, 1, 'Overwrite missing',
                ar.RCaseNature.IMPOSED, ar.RAnalysisType.NON_LIN
            )
            c = self.rb.cases.create_load_case(
                1, 'Overwrite present',
                ar.RCaseNature.WIND, ar.RAnalysisType.NON_LIN, overwrite=True
            )
            self.assertEqual(c.Name, 'Overwrite present')

        with self.subTest(msg='cases.create_load_case (no num)'):
            c = self.rb.cases.create_load_case(
                None, 'No num',
                ar.RCaseNature.SNOW, ar.RAnalysisType.NON_LIN, overwrite=True
            )
            self.assertEqual(c.Name, 'No num')

        for n in ('PERM', 'IMPOSED', 'WIND', 'SNOW', 'ACC'):
            with self.subTest(msg='cases.create_load_case (synonyms)', n=n):
                c = self.rb.cases.create_load_case(
                    None, 'Synonyms', n, ar.RAnalysisType.NON_LIN)
                self.assertEqual(c.Name, 'Synonyms')

        for a in ('LINEAR', 'NON_LIN'):
            with self.subTest(msg='cases.create_combination (synonyms)', a=a):
                c = self.rb.cases.create_load_case(
                    None, 'Synonyms', ar.RCaseNature.SNOW, a)
                self.assertEqual(c.Name, 'Synonyms')

    def test_create_combination(self):
        cs = []
        for i in range(5):
            cs.append(self.rb.cases.create_load_case(
                i + 1, f'case {i + 1}', ar.RCaseNature.PERM,
                ar.RAnalysisType.LINEAR)
            )

        with self.subTest(msg='cases.create_combination'):
            comb = self.rb.cases.create_combination(
                6, 'comb', {i + 1: (i + 1) / 2. for i in range(5)},
                ar.RCombType.SLS, ar.RCaseNature.PERM,
                ar.RAnalysisType.COMB_LINEAR)
            self.assertEqual(comb.Number, 6)
            self.assertEqual(comb.Name, 'comb')
            for i in range(5):
                self.assertEqual(
                    comb.CaseFactors.Get(i + 1).Factor,
                    (i + 1) / 2.)
            self.assertEqual(comb.CombinationType, ar.RCombType.SLS)
            self.assertEqual(comb.Nature, ar.RCaseNature.PERM)
            self.assertEqual(comb.AnalizeType, ar.RAnalysisType.COMB_LINEAR)

        with self.subTest(msg='cases.create_combination (overwrite)'):
            self.assertRaises(
                ar.errors.AutoRobotIdError,
                self.rb.cases.create_combination, 6, 'Overwrite missing',
                {i + 1: (i + 1) / 2. for i in range(5)}, ar.RCombType.SLS,
                ar.RCaseNature.PERM, ar.RAnalysisType.COMB_LINEAR
            )
            comb = self.rb.cases.create_combination(
                6, 'Overwrite present', {},
                ar.RCombType.SLS, ar.RCaseNature.PERM,
                ar.RAnalysisType.COMB_LINEAR, overwrite=True)
            self.assertEqual(comb.Number, 6)
            self.assertEqual(comb.Name, 'Overwrite present')

        with self.subTest(msg='cases.create_combination (no num, no factor)'):
            comb = self.rb.cases.create_combination(
                None, 'No num', {},
                ar.RCombType.SLS, ar.RCaseNature.PERM,
                ar.RAnalysisType.COMB_LINEAR)
            self.assertEqual(comb.Name, 'No num')

        for t in ('SLS', 'ULS'):
            with self.subTest(msg='cases.create_combination (synonyms)'):
                comb = self.rb.cases.create_combination(
                    None, 'Synonyms', {i + 1: (i + 1) / 2. for i in range(5)},
                    t, ar.RCaseNature.PERM, ar.RAnalysisType.COMB_LINEAR)
                self.assertEqual(comb.Name, 'Synonyms')
        for n in ('PERM', 'IMPOSED', 'WIND', 'SNOW', 'ACC'):
            with self.subTest(msg='cases.create_combination (synonyms)'):
                comb = self.rb.cases.create_combination(
                    None, 'Synonyms', {i + 1: (i + 1) / 2. for i in range(5)},
                    ar.RCombType.SLS, n, ar.RAnalysisType.COMB_LINEAR)
                self.assertEqual(comb.Name, 'Synonyms')
        for a in ('COMB_LINEAR', 'COMB_NON_LIN'):
            with self.subTest(msg='cases.create_combination (synonyms)'):
                comb = self.rb.cases.create_combination(
                    None, 'Synonyms', {i + 1: (i + 1) / 2. for i in range(5)},
                    ar.RCombType.SLS, ar.RCaseNature.PERM, a)
                self.assertEqual(comb.Name, 'Synonyms')

    def test_case_get(self):
        self.rb.cases.create_load_case(1, 'Case', 'PERM', 'LINEAR')
        self.rb.cases.create_combination(2, 'Comb', {}, 'SLS', 'PERM',
                                         'COMB_LINEAR')
        self.assertIsInstance(
            self.rb.cases.get(1), ar.RobotOM.IRobotSimpleCase)
        self.assertIsInstance(
            self.rb.cases.get(2), ar.RobotOM.IRobotCaseCombination)
        self.assertEqual(self.rb.cases.get(1).Name, 'Case')
        self.assertEqual(self.rb.cases.get(2).Name, 'Comb')

    def test_case_select(self):
        with self.rb.cases as cases:
            for i in range(1, 5):
                cases.create_load_case(i, f'Case {i}', 'PERM', 'LINEAR')
            for i in range(6, 10):
                cases.create_combination(i, f'Comb {i}', {}, 'ULS', 'IMPOSED',
                                         'COMB_NON_LIN')
        with self.subTest(msg='cases.select range'):
            self.assertListEqual(
                [c.Number for c in self.rb.cases.select('3to9by3')],
                [3, 6, 9]
            )
        with self.subTest(msg='cases.select all'):
            self.assertEqual(
                len(list(self.rb.cases.select('all'))),
                ar.RobotOM.IRobotCollection(self.rb.cases.GetAll()).Count
            )

    def test_case_delete(self):
        with self.rb.cases as cases:
            for i in range(1, 5):
                cases.create_load_case(i, f'Case {i}', 'PERM', 'LINEAR')
            for i in range(6, 10):
                cases.create_combination(i, f'Comb {i}', {}, 'ULS', 'IMPOSED',
                                         'COMB_NON_LIN')
        self.rb.cases.delete('all')
        self.assertListEqual(list(self.rb.cases.select('all')), [])

    # Node server tests

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
