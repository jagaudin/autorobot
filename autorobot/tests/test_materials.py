import unittest

import autorobot as ar
from autorobot.materials import ExtendedMaterialLabel


class TestExtendedMaterialLabel(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)
        cls.rb.materials.load('S275')
        cls.steel_s275 = cls.rb.materials.get('S275')

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def test_properties(self):
        with self.subTest(msg='is_default'):
            self.assertEqual(
                self.steel_s275.is_default,
                self.steel_s275.data.Default)
        with self.subTest(msg='density'):
            self.assertEqual(
                self.steel_s275.density,
                self.steel_s275.data.RO)
        with self.subTest(msg='RO'):
            self.assertEqual(
                self.steel_s275.RO,
                self.steel_s275.data.RO)
        with self.subTest(msg='E'):
            self.assertEqual(
                self.steel_s275.E,
                self.steel_s275.data.E)
        with self.subTest(msg='G'):
            self.assertEqual(
                self.steel_s275.G,
                self.steel_s275.data.Kirchoff)
        with self.subTest(msg='NU'):
            self.assertEqual(
                self.steel_s275.NU,
                self.steel_s275.data.NU)
        with self.subTest(msg='fy'):
            self.assertEqual(
                self.steel_s275.RE,
                self.steel_s275.data.RE)
        with self.subTest(msg='RE'):
            self.assertEqual(
                self.steel_s275.RE,
                self.steel_s275.data.RE)

    def test_data(self):
        self.assertEqual(
            self.steel_s275.data,
            ar.RobotOM.IRobotMaterialData(self.steel_s275.Data))


class TestMaterialServer(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.rb = ar.initialize(visible=False, interactive=False)
        cls.rb.new(ar.RProjType.SHELL)

    @classmethod
    def tearDownClass(cls):
        cls.rb.quit(save=False)

    def tearDown(self):
        self.rb.structure.Clear()

    def test_material_server(self):
        self.assertIsInstance(
            self.rb.materials,
            ar.materials.ExtendedMaterialServer
        )

    def test_get_db_names(self):
        with self.subTest(msg='all names'):
            all_names = [n.lower() for n in self.rb.materials.get_db_names()]
            self.assertIn('steel', all_names)

        with self.subTest(msg='filter'):
            name = self.rb.materials.get_names_db(
                lambda s: s.startswith('C25')
            )
            self.assertEqual(len(name), 1)
            self.assertEqual(name[0][:3], 'C25')

    def test_load(self):
        self.rb.materials.load('STEEL')
        self.assertTrue(self.rb.structure.Labels.Exist(
            ar.RobotOM.IRobotLabelType.I_LT_MATERIAL, 'STEEL'))
        self.rb.materials.delete('STEEL')

    def test_exist(self):
        self.assertFalse(self.rb.materials.exist('CONCR'))
        self.rb.materials.load('CONCR')
        self.assertTrue(self.rb.materials.exist('CONCR'))
        self.rb.materials.delete('CONCR')

    def test_delete(self):
        self.rb.materials.load('TIMBER')
        self.assertTrue(self.rb.materials.exist('TIMBER'))
        self.rb.materials.delete('TIMBER')
        self.assertFalse(self.rb.materials.exist('TIMBER'))

    def test_get(self):
        self.rb.materials.load('STEEL')
        steel = self.rb.materials.get('STEEL')
        self.assertIsInstance(steel, ar.materials.ExtendedMaterialLabel)
        self.assertEqual(steel.data.Name, 'STEEL')
        self.rb.materials.delete('STEEL')

    def test_get_names(self):
        default_mat = self.rb.materials.get_names()
        mat = ['STEEL', 'CONCR', 'ALUM', 'TIMBER']
        for m in mat:
            self.rb.materials.load(m)
        mat.extend(default_mat)
        with self.subTest(msg='all'):
            names = self.rb.materials.get_names()
            self.assertSetEqual(set(names), set(mat))
        with self.subTest(msg='filter'):
            names = self.rb.materials.get_names(lambda s: s.endswith('R'))
            self.assertSetEqual(set(names), {'CONCR', 'TIMBER'})
        for m in mat:
            self.rb.materials.delete(m)
