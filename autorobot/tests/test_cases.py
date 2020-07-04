import unittest
import time
from numpy.random import random

import autorobot as ar


class TestExtendedSimpleCase(unittest.TestCase):

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

    def test_loads(self):
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        bar = self.rb.bars.create(n1, n2)
        case = self.rb.cases.create_case(1, 'case 1', 'PERM', 'LINEAR')
        case.add_self_weight(desc='sw')
        case.add_bar_udl(bar.Number, fx=random(), desc='udl')
        case.add_bar_pl(bar.Number, x=.5, fx=1, is_relative=True, desc='pl')
        loads = case.loads
        self.assertEqual(len(loads), 3)
        self.assertSetEqual(
            set(['sw', 'udl', 'pl']),
            set([d['Description'] for d in loads])
        )
        self.rb.cases.delete('all')

    def test_add_self_weight(self):
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        self.rb.bars.create(n1, n2)
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        other_bar = self.rb.bars.create(n1, n2)
        case = self.rb.cases.create_case(1, 'case 1', 'PERM', 'LINEAR')
        with self.subTest(msg='all'):
            case.add_self_weight(desc='sw')
            rec = case.get(1)
            sel_str = rec.Objects.ToText().strip()
            all_bar_str = (
                self.rb.selections.CreateFull(ar.constants.ROType.BAR)
                .ToText().strip()
            )
            self.assertEqual(sel_str, all_bar_str)
            self.assertEqual(rec.GetValue(ar.constants.RDeadValues.COEFF), 1.)
            self.assertEqual(rec.Description, 'sw')
            self.assertEqual(
                rec.GetValue(ar.constants.RDeadValues.ENTIRE_STRUCT), True)
            case.delete(1)
        with self.subTest(msg='factor'):
            factor = random()
            case.add_self_weight(s=str(other_bar.Number), factor=factor,
                                 desc='sw fact')
            rec = case.get(1)
            sel_str = rec.Objects.ToText().strip()
            self.assertEqual(sel_str, str(other_bar.Number))
            self.assertEqual(
                rec.GetValue(ar.constants.RDeadValues.COEFF), factor)
            self.assertEqual(rec.Description, 'sw fact')
            self.assertEqual(
                rec.GetValue(ar.constants.RDeadValues.ENTIRE_STRUCT), False)
            case.delete(1)
        self.rb.cases.delete('all')

    def test_add_bar_udl(self):
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        bar = self.rb.bars.create(n1, n2)
        case = self.rb.cases.create_case(1, 'case 1', 'PERM', 'LINEAR')
        fx, fy, fz, alpha, beta, gamma, offset_y, offset_z = random((8,))
        case.add_bar_udl(bar.Number, fx=fx, fy=fy, fz=fz,
                         alpha=alpha, beta=beta, gamma=gamma,
                         offset_y=offset_y, offset_z=offset_z,
                         unit=10., unit_angle=1.5, desc='udl')
        rec = case.get(1)
        sel_str = rec.Objects.ToText().strip()
        self.assertEqual(sel_str, str(bar.Number))
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.FX), fx * 10.)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.FY), fy * 10.)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.FZ), fz * 10.)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.ALPHA), alpha * 1.5)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.BETA), beta * 1.5)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.GAMMA), gamma * 1.5)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.IS_LOC), False)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.IS_PROJ), False)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.IS_REL), False)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.OFFSET_Y), offset_y)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarUDLValues.OFFSET_Z), offset_z)
        self.assertEqual(rec.Description, 'udl')
        self.rb.cases.delete('all')

    def test_add_bar_pl(self):
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        bar = self.rb.bars.create(n1, n2)
        case = self.rb.cases.create_case(1, 'case 1', 'PERM', 'LINEAR')
        x, fx, fy, fz, alpha, beta, gamma, offset_y, offset_z = random((9,))
        case.add_bar_pl(bar.Number, x=x, fx=fx, fy=fy, fz=fz,
                        alpha=alpha, beta=beta, gamma=gamma,
                        is_relative=True,
                        offset_y=offset_y, offset_z=offset_z,
                        unit=10., unit_angle=1.5, desc='pl')
        rec = case.get(1)
        sel_str = rec.Objects.ToText().strip()
        self.assertEqual(sel_str, str(bar.Number))
        self.assertEqual(rec.GetValue(ar.constants.RBarPLValues.X), x)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.FX), fx * 10.)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.FY), fy * 10.)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.FZ), fz * 10.)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.ALPHA), alpha * 1.5)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.BETA), beta * 1.5)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.GAMMA), gamma * 1.5)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.IS_LOC), False)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.IS_REL), True)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.OFFSET_Y), offset_y)
        self.assertEqual(
            rec.GetValue(ar.constants.RBarPLValues.OFFSET_Z), offset_z)
        self.assertEqual(rec.Description, 'pl')
        self.rb.cases.delete('all')

    def test_delete(self):
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        bar = self.rb.bars.create(n1, n2)
        case = self.rb.cases.create_case(1, 'case 1', 'PERM', 'LINEAR')
        case.add_self_weight(desc='sw')
        case.add_bar_udl(bar.Number, fx=random(), desc='udl')
        case.add_bar_pl(bar.Number, x=.5, fx=1, is_relative=True, desc='pl')
        self.assertEqual(len(case.loads), 3)
        case.delete(2)
        self.assertEqual(len(case.loads), 2)
        self.assertSetEqual(
            set(['sw', 'pl']),
            set([d['Description'] for d in case.loads])
        )
        case.delete(1)
        self.assertEqual(len(case.loads), 1)
        self.assertSetEqual(
            set(['pl']),
            set([d['Description'] for d in case.loads])
        )
        case.delete(1)
        self.assertEqual(len(case.loads), 0)
        self.rb.cases.delete('all')

    def test_get(self):
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        bar = self.rb.bars.create(n1, n2)
        case = self.rb.cases.create_case(1, 'case 1', 'PERM', 'LINEAR')
        case.add_self_weight(desc='sw')
        case.add_bar_udl(bar.Number, fx=random(), desc='udl')
        case.add_bar_pl(bar.Number, x=.5, fx=1, is_relative=True, desc='pl')
        for i, desc in zip(range(1, 4), ['sw', 'udl', 'pl']):
            load = case.get(i)
            self.assertEqual(load.Description, desc)
        self.rb.cases.delete('all')


class TestCaseServer(unittest.TestCase):

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

    def test_case_server(self):
        self.assertIsInstance(
            self.rb.cases,
            ar.app.ExtendedCaseServer
        )

    def test_create_case(self):
        with self.subTest(msg='create_case'):
            c = self.rb.cases.create_case(1, 'Dummy', ar.RCaseNature.PERM,
                                          ar.RAnalysisType.LINEAR)
            self.assertIsInstance(c, ar.cases.ExtendedSimpleCase)
            self.assertEqual(c.Name, 'Dummy')

        with self.subTest(msg='create_case (overwrite)'):
            self.assertRaises(
                ar.errors.AutoRobotIdError,
                self.rb.cases.create_case, 1, 'Overwrite missing',
                ar.RCaseNature.IMPOSED, ar.RAnalysisType.NON_LIN
            )
            c = self.rb.cases.create_case(
                1, 'Overwrite present',
                ar.RCaseNature.WIND, ar.RAnalysisType.NON_LIN, overwrite=True
            )
            self.assertEqual(c.Name, 'Overwrite present')

        with self.subTest(msg='create_case (no num)'):
            c = self.rb.cases.create_case(
                None, 'No num',
                ar.RCaseNature.SNOW, ar.RAnalysisType.NON_LIN, overwrite=True
            )
            self.assertEqual(c.Name, 'No num')

        for n in ('PERM', 'IMPOSED', 'WIND', 'SNOW', 'ACC'):
            with self.subTest(msg='create_case (synonyms)', n=n):
                c = self.rb.cases.create_case(
                    None, 'Synonyms', n, ar.RAnalysisType.NON_LIN)
                self.assertEqual(c.Name, 'Synonyms')

        for a in ('LINEAR', 'NON_LIN'):
            with self.subTest(msg='create_case (synonyms)', a=a):
                c = self.rb.cases.create_case(
                    None, 'Synonyms', ar.RCaseNature.SNOW, a)
                self.assertEqual(c.Name, 'Synonyms')

    def test_create_combination(self):
        cs = []
        for i in range(5):
            cs.append(self.rb.cases.create_case(
                i + 1, f'case {i + 1}', ar.RCaseNature.PERM,
                ar.RAnalysisType.LINEAR)
            )

        with self.subTest(msg='create_combination'):
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

        with self.subTest(msg='create_combination (overwrite)'):
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

        with self.subTest(msg='create_combination (no num, no factor)'):
            comb = self.rb.cases.create_combination(
                None, 'No num', {},
                ar.RCombType.SLS, ar.RCaseNature.PERM,
                ar.RAnalysisType.COMB_LINEAR)
            self.assertEqual(comb.Name, 'No num')

        for t in ('SLS', 'ULS'):
            with self.subTest(msg='create_combination (synonyms)'):
                comb = self.rb.cases.create_combination(
                    None, 'Synonyms', {i + 1: (i + 1) / 2. for i in range(5)},
                    t, ar.RCaseNature.PERM, ar.RAnalysisType.COMB_LINEAR)
                self.assertEqual(comb.Name, 'Synonyms')
        for n in ('PERM', 'IMPOSED', 'WIND', 'SNOW', 'ACC'):
            with self.subTest(msg='create_combination (synonyms)'):
                comb = self.rb.cases.create_combination(
                    None, 'Synonyms', {i + 1: (i + 1) / 2. for i in range(5)},
                    ar.RCombType.SLS, n, ar.RAnalysisType.COMB_LINEAR)
                self.assertEqual(comb.Name, 'Synonyms')
        for a in ('COMB_LINEAR', 'COMB_NON_LIN'):
            with self.subTest(msg='create_combination (synonyms)'):
                comb = self.rb.cases.create_combination(
                    None, 'Synonyms', {i + 1: (i + 1) / 2. for i in range(5)},
                    ar.RCombType.SLS, ar.RCaseNature.PERM, a)
                self.assertEqual(comb.Name, 'Synonyms')

    def test_get(self):
        self.rb.cases.create_case(1, 'Case', 'PERM', 'LINEAR')
        self.rb.cases.create_combination(2, 'Comb', {}, 'SLS', 'PERM',
                                         'COMB_LINEAR')
        self.assertIsInstance(
            self.rb.cases.get(1), ar.cases.ExtendedSimpleCase)
        self.assertIsInstance(
            self.rb.cases.get(2), ar.RobotOM.IRobotCaseCombination)
        self.assertEqual(self.rb.cases.get(1).Name, 'Case')
        self.assertEqual(self.rb.cases.get(2).Name, 'Comb')

    def test_select(self):
        with self.rb.cases as cases:
            for i in range(1, 5):
                cases.create_case(i, f'Case {i}', 'PERM', 'LINEAR')
            for i in range(6, 10):
                cases.create_combination(i, f'Comb {i}', {}, 'ULS', 'IMPOSED',
                                         'COMB_NON_LIN')
        with self.subTest(msg='select range'):
            self.assertListEqual(
                [c.Number for c in self.rb.cases.select('3to9by3')],
                [3, 6, 9]
            )
        with self.subTest(msg='select all'):
            self.assertEqual(
                len(list(self.rb.cases.select('all'))),
                ar.RobotOM.IRobotCollection(self.rb.cases.GetAll()).Count
            )

    def test_delete(self):
        with self.rb.cases as cases:
            for i in range(1, 5):
                cases.create_case(i, f'Case {i}', 'PERM', 'LINEAR')
            for i in range(6, 10):
                cases.create_combination(i, f'Comb {i}', {}, 'ULS', 'IMPOSED',
                                         'COMB_NON_LIN')
        self.rb.cases.delete('all')
        self.assertListEqual(list(self.rb.cases.select('all')), [])


if __name__ == '__main__':
    unittest.main()
