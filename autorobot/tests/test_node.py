import unittest
from numpy.random import random
from numpy.testing import assert_array_almost_equal

import autorobot as ar


class TestExtendedNode(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def tearDown(self):
        self.rb.structure.Clear()

    def test_extended_node_as_array(self):
        a = random((3,))
        n = self.rb.nodes.create(*a)
        self.assertIsInstance(n, ar.nodes.ExtendedNode)
        assert_array_almost_equal(a, n.as_array())


if __name__ == '__main__':
    unittest.main()
