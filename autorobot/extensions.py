import sys
from abc import ABC
import numpy as np
import time

import autorobot.utils as utils
from .constants import (
    RCaseNature,
    RCaseType,
    RLicense,
    RLicenseStatus,
    ROType,
    RQuitOpt,
)
from .decorators import abstract_attributes
from .errors import (
    AutoRobotIdError,
    AutoRobotLicenseError,
    AutoRobotProjError,
    AutoRobotValueError,
)
from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotBar,
    IRobotBarServer,
    IRobotCase,
    IRobotCaseCombination,
    IRobotCaseServer,
    IRobotCollection,
    IRobotNode,
    IRobotNodeServer,
    IRobotSelectionFactory,
    IRobotSimpleCase,
    RobotApplication,
)

# Get a reference to the module instance
_this = sys.modules[__name__]


class ExtendedRobotApp:
    """This class encapsulates and extends ``RobotApplication``.

    The attributes and methods of the underlying ``RobotApplication`` object
    can be accessed directly through an instance of this class

    :param bool visible:
       Whether the new ``RobotApplication`` is visible (default: ``True``)
    :param bool interactive:
       Whether the new ``RobotApplication`` is interactive (default: ``True``)
    """
    def __init__(self, visible=True, interactive=True):
        """Constructor method."""
        self.app = RobotApplication()
        if not self.has_license:
            self.quit(save=False)
            raise AutoRobotLicenseError()
        if visible:
            self.show(interactive)
        else:
            self.hide()

    @property
    def bars(self):
        """
        Gets the current project's bar server as an instance of
        :py:class:`.ExtendedBarServer`.
        """
        return ExtendedBarServer(self.app.Project.Structure.Bars, self)

    @property
    def cases(self):
        """
        Gets the current project's case server as an instance of
        :py:class:`.ExtendedCaseServer`.
        """
        return ExtendedCaseServer(self.app.Project.Structure.Cases, self)

    @property
    def nodes(self):
        """
        Gets the current project's node server as an instance of
        :py:class:`.ExtendedNodeServer`.
        """
        return ExtendedNodeServer(self.app.Project.Structure.Nodes, self)

    @property
    def select(self):
        """
        Gets the project's selection factory as an instance of
        :py:class:`.ExtendedSelectionFactory`.
        """
        return ExtendedSelectionFactory(self.app.Project.Structure.Selections)

    @property
    def structure(self):
        """
        Gets the current structure as an instance of ``IRobotStructure``.
        """
        return self.app.Project.Structure

    @property
    def has_license(self):
        """
        Returns *True* if the license was activated, *False* otherwise.
        """
        return any((self.LicenseCheckEntitlement(lic) == RLicenseStatus.OK
                    for lic in RLicense))

    def close(self):
        """Closes the project."""
        self.Project.Close()

    def new(self, proj_type):
        """Creates a new project.

        :param int proj_type:
          The type of project to be created.For more detail, see
          :py:class:`autorobot.RProjType`.

        .. tip:: This method supports :ref:`about_synonyms` for the
          **proj_type** arguments. For example: ::

                app.new('SHELL')
        """
        try:
            self.app.Project.New(utils.synonyms[proj_type])
        except Exception:
            raise AutoRobotProjError(
                f"Couldn't create new project with '{proj_type}'."
            )

    def open(self, path):
        """Opens a file with given path (assuming rtd format)."""
        self.app.Project.Open(str(path))

    def quit(self, save=None):
        """Quits the RobotApplication.

        :param bool save: Whether to:

           * save the opened file (``True``)
           * discard changes (``False``)
           * prompt the user (``None``)
        """
        if save is None:
            self.Quit(RQuitOpt.PROMPT)
        elif save:
            self.Quit(RQuitOpt.SAVE)
        else:
            self.Quit(RQuitOpt.DISCARD)

        del self.app
        _this.app = None
        # Now wait a second to avoid file permission issues
        time.sleep(1)

    def save(self):
        """Saves the project if the file name is known.

        :return:
           ``True`` if the save command was executed, ``False`` otherwise
        """
        if self.Project.FileName:
            return self.Project.Save() or True
        return False

    def save_as(self, path):
        """Saves the project to path. The file format is rtd."""
        self.Project.SaveAs(str(path))

    def show(self, interactive=True):
        """Makes the ``RobotApplication`` visible.

        :param bool interactive:
           Whether the ``RobotApplication`` is interactive (default: ``True``)
        """
        self.app.Visible = True
        self.app.Interactive = interactive

    def hide(self):
        """Hides the ``RobotApplication``."""
        self.app.Visible = False
        self.app.Interactive = False

    def __getattr__(self, name):
        if hasattr(self.app, name):
            return getattr(self.app, name)
        raise AttributeError(
            f"{self.__class__.__name__} has not attribute '{name}'.")


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


class ExtendedNode(Capsule):

    _otype = IRobotNode

    def __init__(self, inst):
        """Constructor method."""

        super(ExtendedNode, self).__init__(inst)
        self.node = inst

    def __int__(self):
        """Casts node to ``int``, returning the node's number."""
        return self.Number

    def __str__(self):
        """Casts the node to ``str``."""
        return f'Node {self.Number}: {self.as_array()}'

    def as_array(self):
        """Returns an array with the node's coordinates.

        :return: A numpy array of coordinates
        :rtype: numpy array
        """
        return np.array([self.node.X, self.node.Y, self.node.Z])


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
        sel = self.app.select.Create(self._dtype)
        sel.FromText(str(s))
        if not obj:
            for i in range(sel.Count):
                yield sel.Get(i+1)
        else:
            col = IRobotCollection(self.GetMany(sel))
            for i in range(col.Count):
                yield self._rtype(self._ctype(col.Get(i+1)))


class ExtendedBarServer(ExtendedServer):

    _otype = IRobotBarServer
    _ctype = IRobotBar
    _dtype = ROType.BAR
    _rtype = IRobotBar

    def create(self, start, end, num=None, obj=True, overwrite=False):
        """Creates a new bar between ``start`` and ``end`` nodes.

        :param int start, end: The start and end nodes
        :param int num: The number of the new bar (optional)
        :param bool obj:
           Whether the bar is returned as an object (default: ``True``)
        :param bool overwrite: Whether to overwrite existing objects
        :return: The new bar object or its number

        .. note::

           This method casts the arguments **start** and **end** to ``int``
           before creating the new bar.
        """
        try:
            start, end = (
                n.Number if hasattr(n, 'Number') else int(n)
                for n in (start, end)
            )
        except Exception as e:
            raise AutoRobotValueError(
                f"Couldn't create bar with nodes `{start}` and `{end}`."
            ) from e
        if num is None:
            num = self.FreeNumber
        num = int(num)
        if self.Exist(num):
            if overwrite:
                self.Delete(num)
            else:
                raise AutoRobotIdError(f"Bar with id {num} already exists.")
        self.Create(num, start, end)
        return self.get(num) if obj else num


class ExtendedCaseServer(ExtendedServer):

    _otype = IRobotCaseServer
    _ctype = IRobotCase
    _dtype = ROType.CASE
    _rtype = IRobotCase

    label_prefix = {
        RCaseNature.PERM: 'G',
        RCaseNature.IMPOSED: 'Q',
        RCaseNature.WIND: 'W',
        RCaseNature.SNOW: 'S',
        RCaseNature.ACC: 'A',
    }
    """
    A dictionary providing prefixes for labelling to load cases based on
    their nature. The label is formed of the prefix and the case number. The
    values can be changed to suit preferences. The default prefixes are:

     * ``RCaseNature.PERM``: ``'G'``,
     * ``RCaseNature.IMPOSED``: ``'Q'``,
     * ``RCaseNature.WIND``: ``'W'``,
     * ``RCaseNature.SNOW``: ``'S'``,
     * ``RCaseNature.ACC``: ``'A'``,

    .. caution:: There is a distinction between a load case *label* and its
       *name*. The label of a load cases is usually shorter than its name.
    """

    @staticmethod
    def cast(case):
        """Casts a load case object according to its type.

        :param IRobotCase case: The load case object
        """
        if case.Type == RCaseType.SIMPLE:
            return IRobotSimpleCase(case)
        elif case.Type == RCaseType.COMB:
            return IRobotCaseCombination(case)

    def create_load_case(self, num, name, nature, analysis_type,
                         overwrite=False):
        """Creates a new load case.

        :param int num: The load case number
        :param str name: Name of the load case
        :param int nature: Nature of the load case (see `RCaseNature`)
        :param int analysis_type: Type of analysis (see `RAnalysisType`)
        :param bool overwrite:
           Whether to override if number conflicts with existing data
        :return: The load case object (as a ``IRobotSimpleCase`` instance)

        .. tip:: This method supports :ref:`about_synonyms` for the
          **nature** and **analysis_type** arguments. For example: ::

                create_load_case(1, 'Load case', 'IMPOSED', 'LINEAR')
        """
        if num is None:
            num = self.FreeNumber
        num = int(num)
        if self.Exist(num):
            if overwrite:
                self.Delete(num)
            else:
                raise AutoRobotIdError(f"Case with id {num} already exists.")
        case = IRobotSimpleCase(
            self.CreateSimple(num, name, utils.synonyms[nature],
                              utils.synonyms[analysis_type]))
        case.label = self.label_prefix[utils.synonyms[nature]] + str(num)
        return case

    def create_combination(self, num, name, case_factors, comb_type, nature,
                           analysis_type, overwrite=False):
        """Creates a new load case combination.

        :param int num: The load case number
        :param str name: Name of the combination
        :param dict case_factors: A dict of (case, factor) pairs
        :param int comb_type: The type of the combination (see `RCombType`)
        :param int nature: Nature of the load case (see `RCaseNature`)
        :param int analysis_type: Type of analysis (see `RAnalysisType`)
        :param bool overwrite: Whether to overwrite if case id already exists
        :return:
           The load combination object (as an ``IRobotCaseCombination``
           instance)

        .. tip:: This method supports :ref:`about_synonyms` for the
          **comb_type**, **nature** and **analysis_type** arguments.
          For example: ::

                create_combination(1, 'Comb', 'SLS', 'PERM', 'COMB_LINEAR')
        """
        if num is None:
            num = self.FreeNumber
        num = int(num)
        if self.Exist(num):
            if overwrite:
                self.Delete(num)
            else:
                raise AutoRobotIdError(f"Case with id {num} already exists.")
        comb = IRobotCaseCombination(
            self.CreateCombination(num, name, utils.synonyms[comb_type],
                                   utils.synonyms[nature],
                                   utils.synonyms[analysis_type]))
        for k, v in case_factors.items():
            comb.CaseFactors.New(k, v)
        return comb

    def get(self, n):
        """A method to retrieve load case objects from the server.

        :param int n: The case number

        .. note::

           The function casts the argument **n** to ``int`` before querying
           the server.
        """
        return self.cast(super(ExtendedCaseServer, self).get(n))

    def select(self, s, obj=True):
        """
        Returns an iterator of load case objects referred to in a selection
        string.

        :param str s: A valid selection string
        :param bool obj: Whether to return case objects or cases' numbers
        :return: A generator of the selected load cases
        """
        it = super(ExtendedCaseServer, self).select(s, obj)
        if not obj:
            return it
        else:
            for c in it:
                yield self.cast(c)


class ExtendedNodeServer(ExtendedServer):

    _otype = IRobotNodeServer
    _ctype = IRobotNode
    _dtype = ROType.NODE
    _rtype = ExtendedNode

    def create(self, x, y, z, num=None, obj=True, overwrite=False):
        """Creates a new node from coordinates.

        :param float x, y, z: Coordinates of the new node
        :param int num: The number for the new node
        :param bool obj: Whether to return the node object or its number
        :param bool overwrite: Whether to overwrite existing objects
        :return:
           The new node object (as :py:class:`ExtendedNode`) or its number
           (as ``int``)
        """
        if num is None:
            num = self.FreeNumber
        num = int(num)
        if self.Exist(num):
            if overwrite:
                self.Delete(num)
            else:
                raise AutoRobotIdError(f"Bar with id {num} already exists.")
        self.Create(num, float(x), float(y), float(z))
        return self.get(num) if obj else num


class ExtendedSelectionFactory(Capsule):
    _otype = IRobotSelectionFactory


def initialize(visible=True, interactive=True):
    """Initialize a ``RobotApplication`` object.

    :param bool visible: Whether the application window is displayed
    :param bool interactive: Whether the application window is displayed

    .. note::

       A reference to the ``RobotApplication`` is stored in
       :py:data:`autorobot.extensions.app`.
    """
    _this.app = ExtendedRobotApp(visible, interactive)
    return _this.app


#: A reference to the current ``RobotApplication`` instance
app = None
