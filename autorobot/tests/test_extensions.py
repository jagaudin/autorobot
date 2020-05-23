import os
import unittest
from unittest import TestCase
from tempfile import TemporaryDirectory
from itertools import combinations
import numpy as np
from numpy.random import random

import autorobot as ar


class TestAppOperations(TestCase):

    def test_init_quit(self):
        rb = ar.initialize()
        with self.subTest(msg='rb.Visible'):
            self.assertTrue(rb.Visible)
        with self.subTest(msg='rb.Interactive'):
            self.assertTrue(rb.Interactive)
        rb.quit(save=False)
        with self.subTest(msg='rb.quit'):
            self.assertIsNone(ar.extensions.app)
        rb = ar.initialize(visible=False, interactive=False)
        with self.subTest(msg='rb.Visible'):
            self.assertFalse(rb.Visible)
        with self.subTest(msg='rb.Interactive'):
            self.assertFalse(rb.Interactive)

    def test_new_open_save_close(self):
        '''Tests new, open, save, close methods.'''

        # Customize the __exit__ of the temp dir context to wait a bit
        __exit_orig__ = TemporaryDirectory.__exit__

        def __exit_wait__(self, *args):
            # Wait for the file to unlink before exiting the context
            while True:
                try:
                    return __exit_orig__(self, *args)
                except PermissionError:
                    pass

        TemporaryDirectory.__exit__ = __exit_wait__

        with TemporaryDirectory() as d:
            path = os.path.join(d, 'test_save.rtd')
            rb = ar.initialize(visible=False, interactive=False)
            for pt in ar.RProjType:
                with self.subTest(msg='new', proj_type=pt):
                    rb.new(pt)

            with self.subTest(msg="save_As"):
                rb.save_as(path)
                self.assertTrue(os.path.exists(path))

            with self.subTest(msg="close"):
                rb.close()
                # It would have been nice to test the close method but
                # the event handler OnClose just doesn't work.
                # See https://forums.autodesk.com/t5/robot-structural-analysis-forum/api-onclose-robot-event/td-p/5602676
            rb.quit(save=False)

            rb = ar.initialize(visible=False, interactive=False)
            with self.subTest(msg="open"):
                rb.open(path)
                self.assertEqual(rb.Project.FileName, path)
            rb.nodes.create(0., 0., 0.)
            rb.save()
            rb.quit(save=False)

            rb = ar.initialize(visible=False, interactive=False)
            rb.open(path)
            with self.subTest(msg="save"):
                for c in rb.nodes.get(1).as_array():
                    self.assertAlmostEqual(c, 0.)
            rb.nodes.create(1., 1., 1.)
            rb.quit(save=True)

            rb = ar.initialize(visible=False, interactive=False)
            rb.open(path)
            with self.subTest(msg="quit save"):
                for c in rb.nodes.get(2).as_array():
                    self.assertAlmostEqual(c, 1.)
            rb.close()
            rb.quit(save=False)

    def test_show_hide(self):
        rb = ar.initialize(visible=False, interactive=False)
        with self.subTest(msg='show'):
            self.assertFalse(rb.Visible)
            rb.show()
            self.assertTrue(rb.Visible)

        with self.subTest(msg='hide'):
            self.assertTrue(rb.Visible)
            rb.hide()
            self.assertFalse(rb.Visible)
        rb.quit(save=False)


class TestDataServers(TestCase):

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
            ar.extensions.ExtendedBarServer
        )

    def test_bar_create(self):
        with self.subTest(msg='bars.create (ExtendedNode)'):
            a1, a2 = random((3,)), random((3,))
            n1 = self.rb.nodes.create(*a1)
            n2 = self.rb.nodes.create(*a2)
            self.assertIsInstance(n1, ar.extensions.ExtendedNode)
            self.assertIsInstance(n2, ar.extensions.ExtendedNode)
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
        ns = []
        for i in range(10):
            ns.append(self.rb.nodes.create(*random((3,))))
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

    # Case server test

    def test_case_server(self):
        self.assertIsInstance(
            self.rb.cases,
            ar.extensions.ExtendedCaseServer
        )

    def test_create_load_case(self):
        pass

    def test_create_combination(self):
        pass

    # Node server tests

    def test_node_server(self):
        self.assertIsInstance(
            self.rb.nodes,
            ar.extensions.ExtendedNodeServer
        )


if __name__ == '__main__':
    unittest.main()
