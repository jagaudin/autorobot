import unittest
from random import sample
import numpy as np
from numpy.random import random

import autorobot as ar


class TestSectionServer(unittest.TestCase):

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
        params = [
            ['Rnd Solid', random()],
            ['Rnd Hollow', random() + 1, 0., random(), 'round', False],
            ['Rct Solid', random() * 1e2, random() * 1e2, 0., 'rect'],
            ['Rect Hollow', random() + 1, random() + 1, random() / 1e2, 'rect',
                False],
            ['Unit', random(), 0., 0., 'round', True, '', 1.],
        ]
        # Variable used later for the calculation of rectangles IX
        d0 = params[0][1]
        d1 = params[1][1]
        t1 = params[1][3]
        d2 = params[2][1]
        b2 = params[2][2]
        x2 = max(d2, b2) / 2
        y2 = min(d2, b2) / 2
        d3 = params[3][1]
        b3 = params[3][2]
        t3 = params[3][3]
        d4 = params[4][1] * 1e3
        props = [
            # Expected values for d, b, t, IX, IY, IZ
            [
                d0,
                d0,
                0.,
                np.pi * d0 ** 4 / 32,
                np.pi * d0 ** 4 / 64,
                np.pi * d0 ** 4 / 64,
            ],
            [
                d1,
                d1,
                t1,
                np.pi / 2 * ((d1 / 2) ** 4 - (d1 / 2 - t1) ** 4),
                np.pi / 4 * ((d1 / 2) ** 4 - (d1 / 2 - t1) ** 4),
                np.pi / 4 * ((d1 / 2) ** 4 - (d1 / 2 - t1) ** 4),
            ],
            [
                d2,
                b2,
                0.,
                x2 * y2 ** 3 * (
                    16 / 3 - 3.36 * y2 / x2 * (1 - y2 ** 4 / 12 / x2 ** 4)
                ),
                d2 ** 3 * b2 / 12,
                d2 * b2 ** 3 / 12,
            ],
            [
                d3,
                b3,
                t3,
                2 * t3 * (d3 - t3) ** 2 * (b3 - t3) ** 2 / (d3 + b3 - 2 * t3),
                (d3 ** 3 * b3 - (d3 - 2 * t3) ** 3 * (b3 - 2 * t3)) / 12,
                (d3 * b3 ** 3 - (d3 - 2 * t3) * (b3 - 2 * t3) ** 3) / 12,
            ],
            [
                d4,
                d4,
                0.,
                np.pi * d4 ** 4 / 32,
                np.pi * d4 ** 4 / 64,
                np.pi * d4 ** 4 / 64,
            ],
        ]
        for param, prop in zip(params, props):
            with self.subTest(name=param[0]):
                self.rb.sections.create(*param)
                label = self.rb.sections.get(param[0])
                self.assertIsInstance(label, ar.sections.ExtendedSectionLabel)
                self.assertAlmostEqual(label.d * 1e3, prop[0])
                self.assertAlmostEqual(label.b * 1e3, prop[1])
                self.assertAlmostEqual(label.t * 1e3, prop[2])
                # Test relative difference for I values as Robot may give
                # slightly different values.
                self.assertAlmostEqual(
                    (label.IX * 1e12 - prop[3]) / prop[3], 0., delta=5e-3)
                self.assertAlmostEqual(
                    (label.IY * 1e12 - prop[4]) / prop[3], 0., delta=5e-3)
                self.assertAlmostEqual(
                    (label.IZ * 1e12 - prop[5]) / prop[3], 0., delta=5e-3)

    def test_set(self):
        self.rb.sections.create('Rnd10', 10.)
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        b = self.rb.bars.create(n1, n2)
        self.rb.sections.set('all', 'Rnd10')
        for b in self.rb.bars.select('all'):
            label = ar.RobotOM.IRobotLabel(
                b.GetLabel(ar.RobotOM.IRobotLabelType.I_LT_BAR_SECTION))
            self.assertEqual(label.Name, 'Rnd10')

    def test_db_list(self):
        with self.subTest(msg='no filter'):
            self.assertIn('AISC', self.rb.sections.db_list())
            self.assertIn('EURO', self.rb.sections.db_list())
        with self.subTest(msg='filter'):
            dbs = self.rb.sections.db_list(lambda s: False)
            self.assertEqual(len(dbs), 0)

    def test_get_db(self):
        name = self.rb.sections.db_list()[0]
        db = self.rb.sections.get_db(name)
        self.assertIsInstance(db, ar.RobotOM.IRobotSectionDatabase)

    def test_get_db_names(self):
        with self.subTest(msg='no filter'):
            db_name = self.rb.sections.db_list()[0]
            names = self.rb.sections.get_db_names(db_name)
            for name in sample(names, 10):
                self.rb.sections.load(name, db_name)
                self.assertTrue(self.rb.sections.exist(name))
                self.rb.sections.delete(name)
        with self.subTest(msg='filter'):
            names = self.rb.sections.get_db_names(db_name, lambda s: False)
            self.assertEqual(len(names), 0)

    def test_load(self):
        with self.subTest(msg='no database'):
            db_name = self.rb.sections.db_list()[0]
            name = self.rb.sections.get_db_names(db_name)[0]
            self.rb.sections.load(name)
            self.assertTrue(self.rb.sections.exist(name))
            self.rb.sections.delete(name)
        with self.subTest(msg='no database'):
            db_name = self.rb.sections.db_list()[0]
            name = self.rb.sections.get_db_names(db_name)[0]
            self.rb.sections.load(name, db_name)
            self.assertTrue(self.rb.sections.exist(name))
            self.rb.sections.delete(name)

    def test_get(self):
        self.rb.sections.load('HP 12x63')
        hp_1263 = self.rb.sections.get('HP 12x63')
        self.assertIsInstance(hp_1263, ar.sections.ExtendedSectionLabel)
        self.assertEqual(hp_1263.data.Name, 'HP 12x63')
        self.rb.sections.delete('HP 12x63')

    def test_get_names(self):
        pass

    def test_delete(self):
        self.rb.sections.load('HP 12x63')
        self.assertTrue(self.rb.sections.exist('HP 12x63'))
        self.rb.sections.delete('HP 12x63')
        self.assertFalse(self.rb.sections.exist('HP 12x63'))

    def test_exist(self):
        self.assertFalse(self.rb.sections.exist('HP 12x63'))
        self.rb.sections.load('HP 12x63')
        self.assertTrue(self.rb.sections.exist('HP 12x63'))
        self.rb.sections.delete('HP 12x63')
