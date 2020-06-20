import unittest
import numpy as np
from numpy.random import random

import autorobot as ar


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
            alpha, beta, gamma =  180 * random((3,))
            label = self.rb.supports.create(
                'angles', '101010',
                alpha = alpha,
                beta = beta,
                gamma = gamma
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
            alpha, beta, gamma, unit_force, unit_angle  = random((5,))
            label = self.rb.supports.create(
                'units', '010101',
                elasticity = elasticity,
                alpha = alpha,
                beta = beta,
                gamma = gamma,
                unit_force = unit_force,
                unit_angle = unit_angle,
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
