from abc import ABC
from functools import wraps

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
    """
    A class to encapsulate an instance of a specific type.

    The ``Capsule`` class allow reaad/write access to existing attributes of
    the encapsulated instance.
    """

    def __init__(self, inst):
        """Initialize a Capsule instance.

        :param obj inst: An object instance

        .. note::

           The instance must be of type ``_otype``.
        """
        self._inst = inst
        if not isinstance(inst, self._otype):
            raise AutoRobotValueError(
                f"{inst} is not an instance of `{str(self._otype)}`.")

    def __getattr__(self, name):
        """Custom attribute getter looking up the instance object.

        :param str name: The name of the attribute
        :return: The encapsulated instance attribute with name
        :raise AttributeError: When the encapsulated instance lookup fails
        """
        # Called when the default attribute access fails
        if name != '_inst' and hasattr(self._inst, name):
            return getattr(self._inst, name)
        raise AttributeError(
            f"{self.__class__.__name__} has no attribute '{name}'.")

    def __setattr__(self, name, value):
        """Custom attribute getter looking up the instance object.

        When the encapsulated instance has an attribute of the requested
        ``name`` and the Capsule object doesn't, the instance attribute
        is set to ``value``. Otherwise, the attribute is set on the Capsule
        object.

        :param str name: The name of the attribute
        :param obj value: The value for the attribute
        """
        if (hasattr(self, '_inst') and
                hasattr(self._inst, name) and name not in dir(self)):
            setattr(self._inst, name, value)
        else:
            super().__setattr__(name, value)


@abstract_attributes('_otype', '_ctype', '_dtype', '_rtype')
class ExtendedServer(Capsule, ABC):
    """
    A class to encapsulate an RSA data server.

    A class inheriting from ``ExtendedServer`` must define the following
    class attributes:

        * ``_otype``: The type of the server instance
        * ``_ctype``: The casting type for the content (e.g. ``IRobotBar``)
        * ``_dtype``: The data type of the content (see ``IRobotObjectType``)
        * ``_rtype``: The type returned by queries (e.g. ``ExtendedBar``)

    """

    def __init__(self, inst, app):
        """
        Initializes an ``ExtendedServer`` instance.

        :param obj inst: The server instance
        :param obj app: The application instance
        """
        super(ExtendedServer, self).__init__(inst)
        self.app = app
        self.server = inst

    def __enter__(self):
        """Enters a context where operations on the server are grouped."""
        if hasattr(self.server, 'BeginMultiOperation'):
            self.server.BeginMultiOperation()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        """Exits a context where operations on the server are grouped."""
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
        """Deletes a selection of objects.

        :param str s: A valid selection string
        """
        sel = self.app.selections.Create(self._dtype)
        sel.FromText(str(s))
        self.DeleteMany(sel)


@abstract_attributes('_otype', '_dtype')
class ExtendedLabel(Capsule, ABC):
    """
    A class to encapsulate an ``IRobotLabel`` instance.

    A class inheriting from ``ExtendedLabel`` must define the following
    class attributes:

        * ``_otype``: ``IRobotLabel`` invariably
        * ``_dtype``: The type of the data associated with the label

    """
    @property
    def data(self):
        """The data associated with the label instance."""
        return self._dtype(self.Data)

    def __str__(self):
        """The string representation of a label."""
        return self.Name


@abstract_attributes('_otype', '_ctype', '_ltype', '_dtype', '_rtype')
class ExtendedLabelServer(Capsule, ABC):
    """
    A class to encapsulate an ``IRobotLabelServer`` instance.

    A class inheriting from ``ExtendedLabelServer`` must define the following
    class attributes:

        * ``_otype``: ``IRobotLabelServer`` invariably
        * ``_ctype``: ``IRobotLabel`` invariably
        * ``_ltype``: The label type of the content (see ``IRobotLabelType``)
        * ``_dtype``: The data type associated with the labels
        * ``_rtype``:
            The type returned by queries (e.g. ``ExtendedSupportLabel``)

    """

    def __init__(self, inst, app):
        """
        Initializes an ``ExtendedLabelServer`` instance.

        :param obj inst: The server instance
        :param obj app: The application instance
        """
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


class EnumCapsule(dict):
    """
    A class to encapsulate Enum object as translated by PythonNet > 3.

    An EnumCapsule instance is a dictionary instance with the following
    additional properties:

        * The keys of the dictionary can be queried with an attribute notation.
        * When iterated over, the dictionary yields a set of unique values, as
          a Python Enum would.
        * During initialization, the original Enum content is added to the
          dictionary.
        * The ``custom_index`` property is a dictionary with keys not present
          in the original Enum.
        * Can be called to obtain an arbitrary Enum value of the correct type.

    This is so far the best way to provide an intuitive use of Enums but may
    have to be reconsidered at a later stage.
    """

    def __init__(self, enum, custom_index=None):
        """
        Initializes an ``EnumCapsule`` instance.

        :param obj enum: The original Enum
        :param dict custom_index: A dictionary with additional keys
        """
        super().__init__(self)
        self._inst = enum
        self._custom_index = {}
        self.update(custom_index)

    def __getattr__(self, name):
        """Custom attribute getter looking up the dictionary & instance object.

        :param str name: The name of the attribute
        :return: The corresponding dictionary value or instance attribute
        :raise AttributeError: When the encapsulated instance lookup fails
        """
        if name in self.keys():
            return self[name]
        if name != '_inst' and hasattr(self._inst, name):
            return getattr(self._inst, name)
        raise AttributeError(
            f"{self.__class__.__name__} has no attribute '{name}'.")

    def __iter__(self):
        """Yields from the set of unique dictionary values."""
        yield from self.unique_values()

    def __call__(self, value, unchecked=True):
        """
        An ``EnumCapsule`` instance can be called to create arbitrary values.

        :param int value: An arbitrary value
        :param bool unchecked: Must be True if value is not already defined.
        """
        return self._inst(value, unchecked)

    @property
    def custom_index(self):
        """A sub-dictionary with all non-original keys."""
        return self._custom_index

    def update(self, custom_index=None):
        """Updates the dictionary with another.

        :param dict custom_index: A dictionary with custom keys

        .. note::
           The original Enum values will be added to the dictionary
           automatically and an attempt will be made to convert the
           **custom_index** values to the appropriate Enum type.
        """
        index = {k: getattr(self._inst, k) for k in self.GetNames(self._inst)}

        if isinstance(custom_index, dict):
            for k, v in custom_index.items():
                if isinstance(v, str) and v in index:
                    custom_index[k] = index[v]
                elif isinstance(v, int):
                    custom_index[k] = self._inst(v, True)

        self._custom_index.update(custom_index)
        index.update(custom_index)
        super().update(index)

    def unique_values(self):
        """
        Returns a list of unique values contained in the dictionary.

        .. note::

           Some Enum members may return a **hash** value of -1, which signifies
           **NotImplementedError** in Python. Therefore, ``set(self.values())``
           may result in an error and it is necessary to write our own method
           to get unique values.
        """
        int_codes = set()
        unique_values = []
        for val in self.values():
            if int(val) not in int_codes:
                int_codes.add(int(val))
                unique_values.append(val)
        return unique_values
