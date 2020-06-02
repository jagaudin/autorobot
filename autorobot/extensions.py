from abc import ABC

from .decorators import abstract_attributes
from .errors import (
    AutoRobotValueError,
)
from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotCollection,
)


@abstract_attributes('_otype')
class Capsule(ABC):
    def __init__(self, inst):
        self._inst = inst
        if not isinstance(inst, self._otype):
            raise AutoRobotValueError(
                f"{inst} is not an instance of `{str(self._otype)}`.")

    def __getattr__(self, name):
        if hasattr(self._inst, name):
            return getattr(self._inst, name)
        raise AttributeError(
            f"{self.__class__.__name__} has not attribute '{name}'.")


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
