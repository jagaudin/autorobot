import unittest

from abc import ABC
from random import randrange

import autorobot as ar

from autorobot.decorators import (
    defaults_to_none,
    requires_init,
    abstract_attributes
)

from autorobot.errors import AutoRobotInitError, COMException


class test_default_to_none(unittest.TestCase):

    def test_returns_none(self):
        @defaults_to_none
        def f():
            raise COMException

        self.assertIs(f(), None)


class test_requires_init(unittest.TestCase):

    def test_raises_init_error(self):
        @requires_init
        def f():
            return

        assert(ar.app.app == None)
        with self.assertRaises(AutoRobotInitError):
            f()

        ar.app.app = True
        self.assertEqual(f(), None)
        ar.app.app = None


class test_abstract_attributes(unittest.TestCase):

    def test_raises_not_implemented_error(self):
        @abstract_attributes('_test')
        class Parent(ABC):
            pass

        with self.assertRaises(NotImplementedError):
            class Child(Parent):
                pass

        class Child(Parent):
            _test = None

        self.assertTrue(hasattr(Child(), '_test'))
