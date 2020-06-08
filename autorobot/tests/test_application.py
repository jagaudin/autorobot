import os
import time
import unittest
from unittest import TestCase
from tempfile import TemporaryDirectory
import numpy as np
from numpy.testing import assert_array_almost_equal

import autorobot as ar


class TestAppOperations(TestCase):

    def test_init_quit(self):
        """Tests initialize and quit methods."""

        rb = ar.initialize()
        with self.subTest(msg='rb.has_license'):
            self.assertTrue(rb.has_license)
        with self.subTest(msg='rb.Visible'):
            self.assertTrue(rb.Visible)
        with self.subTest(msg='rb.Interactive'):
            self.assertTrue(rb.Interactive)
        rb.quit(save=False)
        with self.subTest(msg='rb.quit'):
            self.assertIsNone(ar.app.app)
        rb = ar.initialize(visible=False, interactive=False)
        with self.subTest(msg='rb.Visible'):
            self.assertFalse(rb.Visible)
        with self.subTest(msg='rb.Interactive'):
            self.assertFalse(rb.Interactive)

    def test_new_open_save_close(self):
        """Tests new, open, save and close methods."""

        # Customize the __exit__ of the temp dir context
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
                    self.assertEqual(rb.Project.Type, pt)
                # Wait for Robot to avoid throwing a server error
                time.sleep(0.5)

            for pt in ('BUILDING', 'FRAME_2D', 'FRAME_3D', 'SHELL',
                       'TRUSS_2D', 'TRUSS_3D'):
                with self.subTest(msg='new (synomyms)', proj_type=pt):
                    rb.new(pt)
                    self.assertEqual(
                        rb.Project.Type, ar.synonyms.synonyms[pt])
                    # Wait for Robot to avoid throwing a server error
                    time.sleep(.5)

            with self.subTest(msg="save_As"):
                rb.save_as(path)
                self.assertTrue(os.path.exists(path))

            with self.subTest(msg="close"):
                rb.close()
                # It would have been nice to test the close method but
                # the event handler OnClose just doesn't work.
                # See https://forums.autodesk.com/t5/robot-structural-analysis-forum/api-onclose-robot-event/td-p/5602676  # NOQA
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
                assert_array_almost_equal(
                    rb.nodes.get(1).as_array(), np.zeros((3,)))
            rb.nodes.create(1., 1., 1.)
            rb.quit(save=True)

            rb = ar.initialize(visible=False, interactive=False)
            rb.open(path)
            with self.subTest(msg="quit save"):
                assert_array_almost_equal(
                    rb.nodes.get(2).as_array(), np.ones((3,)))
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


if __name__ == '__main__':
    unittest.main()
