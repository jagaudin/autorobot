import os
import unittest
import time
from unittest import TestCase
from tempfile import TemporaryDirectory
from shutil import copyfile

import autorobot as ar

class TestExtendedApp(TestCase):
    
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
            
    def test_new_open_save(self):
        with TemporaryDirectory() as d:
            path = os.path.join(d, 'test_save.rtd')
            rb = ar.initialize(visible=False, interactive=False)
            for pt in ar.RProjType:
                with self.subTest(proj_type=pt):
                    rb.new(pt)
            rb.save_as(path)
            with self.subTest(msg="save_As"):
                self.assertTrue(os.path.exists(path))
            rb.close()
            with self.subTest(msg="close 1"):
                self.assertRaises(AttributeError, lambda : self.Project.Filename)
            rb.quit(save=False)
            with self.subTest(msg="rb.quit 1"):
                self.assertIsNone(ar.extensions.app)
            # Wait before restart
            time.sleep(10)
            for i in range(5):
                cp_path = os.path.join(d, f'test_save{i}.rtd')
                copyfile(path, cp_path)
            rb = ar.initialize(visible=False, interactive=False)
            with self.subTest(msg="initialize 1"):
                self.assertIsNotNone(ar.extensions.app)
            rb.open(cp_path)
            with self.subTest(msg="open 1"):
                self.assertEqual(rb.Project.Filename, cp_path)
            rb.nodes.create(0., 0., 0.)
            with self.subTest(msg="node 1"):
                for c in rb.nodes.get(1).to_array():
                    self.assertAlmostEqual(c, 0.)
            rb.save()
            rb.close()
            with self.subTest(msg="close"):
                self.assertRaises(AttributeError, lambda : self.Project.Filename)
            rb.open(path)
            with self.subTest(msg="open 2"):
                self.assertEqual(rb.Project.Filename, path)
            with self.subTest(msg="save"):
                for c in rb.nodes.get(1).to_array():
                    self.assertAlmostEqual(c, 0.)
            rb.nodes.create(1., 1., 1.)
            with self.subTest(msg="node 2"):
                for c in rb.nodes.get(1).to_array():
                    self.assertAlmostEqual(c, 1.)
            rb.quit(save=True)
            with self.subTest(msg="rb.quit 1"):
                self.assertIsNone(ar.extensions.app)
            # Wait before restart
            time.sleep(5)
            rb = ar.initialize(visible=False, interactive=False)
            with self.subTest(msg="initialize 2"):
                self.assertIsNotNone(ar.extensions.app)
            rb.open(path)
            with self.subTest(msg="open 3"):
                self.assertEqual(rb.Project.Filename, path)
            with self.subTest(msg="quit save"):
                for c in rb.nodes.get(2).to_array():
                    self.assertAlmostEqual(c, 1.)
            
            
if __name__ == '__main__':
    unittest.main()