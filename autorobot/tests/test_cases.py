import unittest

import autorobot as ar


class TestCaseServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
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


if __name__ == '__main__':
    unittest.main()
