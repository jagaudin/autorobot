import unittest
import numpy as np
from numpy.random import random

import autorobot as ar


class TestExtendedSupport(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def test_properties(self):
        label = self.rb.supports.create('test_properties', '000000')
        with self.subTest(msg='UX'):
            self.assertFalse(label.UX)
        with self.subTest(msg='UY'):
            self.assertFalse(label.UY)
        with self.subTest(msg='UZ'):
            self.assertFalse(label.UZ)
        with self.subTest(msg='RX'):
            self.assertFalse(label.RX)
        with self.subTest(msg='RY'):
            self.assertFalse(label.RY)
        with self.subTest(msg='RZ'):
            self.assertFalse(label.RZ)
        self.rb.supports.delete('test_properties')
        label = self.rb.supports.create('test_properties', '111111')
        with self.subTest(msg='UX'):
            self.assertTrue(label.UX)
        with self.subTest(msg='UY'):
            self.assertTrue(label.UY)
        with self.subTest(msg='UZ'):
            self.assertTrue(label.UZ)
        with self.subTest(msg='RX'):
            self.assertTrue(label.RX)
        with self.subTest(msg='RY'):
            self.assertTrue(label.RY)
        with self.subTest(msg='RZ'):
            self.assertTrue(label.RZ)
        self.rb.supports.delete('test_properties')


class TestSupportServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)
        cls.n1 = cls.rb.nodes.create(*random((3,)))
        cls.n2 = cls.rb.nodes.create(*random((3,)))

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def test_create(self):
        with self.subTest(msg='angles'):
            alpha, beta, gamma = 180 * random((3,))
            label = self.rb.supports.create(
                'angles', '101010', alpha=alpha, beta=beta, gamma=gamma
            )
            self.assertEqual(label.Name, 'angles')
            self.assertTrue(label.UX)
            self.assertFalse(label.UY)
            self.assertTrue(label.UZ)
            self.assertFalse(label.RX)
            self.assertTrue(label.RY)
            self.assertFalse(label.RZ)
            self.assertAlmostEqual(label.data.Alpha, alpha * np.pi / 180)
            self.assertAlmostEqual(label.data.Beta, beta * np.pi / 180)
            self.assertAlmostEqual(label.data.Gamma, gamma * np.pi / 180)
            self.rb.supports.delete('angles')

        with self.subTest(msg='units'):
            elasticity = random((6,))
            alpha, beta, gamma, unit_force, unit_angle = random((5,))
            label = self.rb.supports.create(
                'units', '010101',
                elasticity=elasticity,
                alpha=alpha,
                beta=beta,
                gamma=gamma,
                unit_force=unit_force,
                unit_angle=unit_angle,
            )
            self.assertEqual(label.Name, 'units')
            self.assertFalse(label.UX)
            self.assertTrue(label.UY)
            self.assertFalse(label.UZ)
            self.assertTrue(label.RX)
            self.assertFalse(label.RY)
            self.assertTrue(label.RZ)
            self.assertAlmostEqual(label.data.KX, elasticity[0] * unit_force)
            self.assertAlmostEqual(label.data.KY, elasticity[1] * unit_force)
            self.assertAlmostEqual(label.data.KZ, elasticity[2] * unit_force)
            self.assertAlmostEqual(label.data.HX,
                                   elasticity[3] * unit_force / unit_angle)
            self.assertAlmostEqual(label.data.HY,
                                   elasticity[4] * unit_force / unit_angle)
            self.assertAlmostEqual(label.data.HZ,
                                   elasticity[5] * unit_force / unit_angle)
            self.assertAlmostEqual(label.data.Alpha, alpha * unit_angle)
            self.assertAlmostEqual(label.data.Beta, beta * unit_angle)
            self.assertAlmostEqual(label.data.Gamma, gamma * unit_angle)
            self.rb.supports.delete('units')

        with self.subTest(msg='nodes'):
            v = self.n2.as_array() - self.n1.as_array()
            v_norm = v / np.linalg.norm(v)
            alpha = np.arctan2(v_norm[1], v_norm[0])
            beta = np.arccos(v_norm[2])
            gamma = 0.
            label = self.rb.supports.create(
                'nodes', '111111', node=self.n1, orient_node=self.n2)
            self.assertEqual(label.Name, 'nodes')
            self.assertTrue(label.UX)
            self.assertTrue(label.UY)
            self.assertTrue(label.UZ)
            self.assertTrue(label.RX)
            self.assertTrue(label.RY)
            self.assertTrue(label.RZ)
            self.assertAlmostEqual(label.data.Alpha, alpha)
            self.assertAlmostEqual(label.data.Beta, beta)
            self.assertAlmostEqual(label.data.Gamma, gamma)
            self.rb.supports.delete('nodes')

    def test_set(self):
        self.rb.supports.create('test_set', '111111')
        self.rb.supports.set('all', 'test_set')
        for n in self.rb.nodes.select('all'):
            label = ar.RobotOM.IRobotLabel(
                n.GetLabel(ar.RobotOM.IRobotLabelType.I_LT_SUPPORT))
            self.assertEqual(label.Name, 'test_set')
        self.rb.supports.delete('test_set')

    def test_get(self):
        self.rb.supports.create('test_get', '000111')
        label = self.rb.supports.get('test_get')
        self.assertIsInstance(label, ar.supports.ExtendedSupportLabel)
        self.assertEqual(label.Name, 'test_get')
        self.rb.sections.delete('test_get')

    def test_get_names(self):
        supports = self.rb.supports.get_names()
        self.assertGreater(len(supports), 0)
        new_support = 'test_get_names'
        self.rb.supports.create(new_support, '110000')
        supports.append(new_support)
        with self.subTest(msg='all'):
            names = self.rb.supports.get_names()
            self.assertSetEqual(set(names), set(supports))
        with self.subTest(msg='filter'):
            names = self.rb.supports.get_names(lambda s: False)
            self.assertEqual(len(names), 0)
        self.rb.supports.delete(new_support)

    def test_delete(self):
        self.rb.supports.create('test_delete', '001111')
        self.assertTrue(self.rb.supports.exist('test_delete'))
        self.rb.supports.delete('test_delete')
        self.assertFalse(self.rb.supports.exist('test_delete'))

    def test_exist(self):
        self.assertFalse(self.rb.supports.exist('test_exist'))
        self.rb.supports.create('test_exist', '100000')
        self.assertTrue(self.rb.supports.exist('test_exist'))
        self.rb.supports.delete('test_exist')
