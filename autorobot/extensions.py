from abc import ABC

from .decorators import abstract_attributes
from .errors import (
    AutoRobotValueError,
)
from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotCollection,
    IRobotNamesArray,
)


@abstract_attributes('_otype')
class Capsule(ABC):
    def __init__(self, inst):
        self._inst = inst
        if not isinstance(inst, self._otype):
            raise AutoRobotValueError(
                f"{inst} is not an instance of `{str(self._otype)}`.")

    def __getattr__(self, name):
        # Called when the default attribute access fails
        if name != '_inst' and hasattr(self._inst, name):
            return getattr(self._inst, name)
        raise AttributeError(
            f"{self.__class__.__name__} has not attribute '{name}'.")

    def __setattr__(self, name, value):
        if (hasattr(self, '_inst') and
                hasattr(self._inst, name) and name not in dir(self)):
            setattr(self._inst, name, value)
        else:
            super().__setattr__(name, value)


@abstract_attributes('_otype', '_ctype', '_dtype', '_rtype')
class ExtendedServer(Capsule, ABC):

    def __init__(self, inst, app):
        super(ExtendedServer, self).__init__(inst)
        self.app = app
        self.server = inst

    def __enter__(self):
        if hasattr(self.server, 'BeginMultiOperation'):
            self.server.BeginMultiOperation()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if hasattr(self.server, 'EndMultiOperation'):
            self.server.EndMultiOperation()

    def get(self, n):
        """Returns the object with id number `n` from the server.

        :param int n: The object's number

        .. note::

           The function casts the argument **n** to ``int`` before querying
           the server.
        """
        try:
            return self._rtype(self._ctype(self.server.Get(int(n))))
        except Exception as e:
            raise AutoRobotValueError(
                f"{self.__class__.__name__} couldn't get id `{n}`."
            ) from e

    def select(self, s, obj=True):
        """
        Returns an iterator of objects referred to by numbers in a selection
        string.

        :param str s: A valid selection string
        :param bool obj: Whether to return the objects or their numbers.
        :return: A generator of the selected objects
        """
        sel = self.app.selections.Create(self._dtype)
        sel.FromText(str(s))
        if not obj:
            for i in range(sel.Count):
                yield sel.Get(i+1)
        else:
            col = IRobotCollection(self.GetMany(sel))
            for i in range(col.Count):
                yield self._rtype(self._ctype(col.Get(i+1)))

    def delete(self, s):
        """Deletes a sa selection of objects.

        :param str s: A valid selction string
        """
        sel = self.app.selections.Create(self._dtype)
        sel.FromText(str(s))
        self.DeleteMany(sel)


@abstract_attributes('_otype', '_dtype')
class ExtendedLabel(Capsule, ABC):

    @property
    def data(self):
        return self._dtype(self.Data)

    def __str__(self):
        return self.Name


@abstract_attributes('_otype', '_ctype', '_ltype', '_dtype', '_rtype')
class ExtendedLabelServer(Capsule, ABC):

    def __init__(self, inst, app):
        super(ExtendedLabelServer, self).__init__(inst)
        self.app = app
        self.server = inst

    def get(self, name):
        """Returns the label with name **name** from the server.

        :param str name: The name of the label
        """
        try:
            return self._rtype(
                self._ctype(self.server.Get(self._ltype, str(name))))
        except Exception as e:
            raise AutoRobotValueError(
                f"{self.__class__.__name__} couldn't get id `{name}`."
            ) from e

    def get_names(self, func=lambda s: True):
        """Returns the names available in the current stucture.

        :param function func: A filter function
        :return: The list of label names in the structure
        """
        names = IRobotNamesArray(self.GetAvailableNames(self._ltype))
        names = [names.Get(i) for i in range(1, names.Count + 1)]
        return [name for name in names if func(name)]

    def delete(self, name):
        """Deletes a label from the structure.

        :param str name: The name of the label to delete
        """
        self.Delete(self._ltype, name)

    def exist(self, name):
        """Checks whether a label with the given name exists in the structure.

        :param str name: The name of the label
        """
        return self.Exist(self._ltype, name)
