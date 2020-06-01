from unittest import TestCase
from random import random


class TestSections(TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)
        n1 = self.rb.nodes.create(*random((3,)))
        n2 = self.rb.nodes.create(*random((3,)))
        cls.b = self.rb.bars.create(n1, n2)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def test_create_section(self):
        params = {
            0: ['Rnd Solid', random()]
            1: ['Rnd Hollow', random(), 0., random(), 'round', False]
            2: ['Rct Solid', random(), random(), 0., 'rect']
            3: ['Rct Hollow', random(), random(), random(), 'rect', False]
            4: ['Unit', random(), 0., 0., 'round', True, '1.']
        }
        for param in params.items():
            with self.subTest(name=param[0]):
                self.rb.create_section(*param)
