import numpy as np

from .materials import ExtendedMaterialLabel
from .sections import ExtendedSectionLabel
from .releases import ExtendedReleaseLabel

from .constants import (
    RLabelType,
    ROType,
)

from .decorators import defaults_to_none

from .extensions import (
    Capsule,
    ExtendedServer,
)

from .errors import (
    AutoRobotIdError,
    AutoRobotValueError,
)

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotBar,
    IRobotBarServer,
    IRobotLabel,
)


class ExtendedBar(Capsule):
    """
    This class is an extension for ``IRobotBar`` providing the properties
    listed below in addition to the methods of the original object.
    """

    _otype = IRobotBar

    def __init__(self, inst):
        """Constructor method."""
        super(ExtendedBar, self).__init__(inst)
        self.bar = inst

    @property
    @defaults_to_none
    def material(self):
        """Material of the bar."""
        # Robot assigns a material by default, its anme is '' (empty string)
        # Characteristics of this material are mostly set to zero.
        # For consistency, we return None in this case. To get the no-name
        # material label, use the ``IRobotBar.GetLabel`` method
        label = ExtendedMaterialLabel(
            IRobotLabel(self.GetLabel(RLabelType.MAT)))
        return label if label.Name else None

    @material.setter
    def material(self, name):
        self.SetLabel(RLabelType.MAT, name)

    @property
    @defaults_to_none
    def section(self):
        """Section of the bar."""
        return ExtendedSectionLabel(
            IRobotLabel(self.GetLabel(RLabelType.BAR_SECT)))

    @section.setter
    def section(self, name):
        self.SetLabel(RLabelType.BAR_SECT, name)

    @property
    @defaults_to_none
    def release(self):
        """Release of the bar."""
        return ExtendedReleaseLabel(
            IRobotLabel(self.GetLabel(RLabelType.RELEASE)))

    @release.setter
    def release(self, name):
        self.SetLabel(RLabelType.RELEASE, name)


class ExtendedBarServer(ExtendedServer):
    """
    This class is an extension for ``IRobotBarServer`` providing
    additional functions for the management of bars.
    """

    _otype = IRobotBarServer
    _ctype = IRobotBar
    _dtype = ROType.BAR
    _rtype = ExtendedBar

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

    def table(self, s):
        """Returns a 2d array containing bar numbers and connected nodes.

        :param str s: A valid selection string
        :return:
           A 2d array with the bars' number, start and end nodes.
        """
        return np.stack([
            np.array([b.Number, b.StartNode, b.EndNode])
            for b in self.select(s)
        ])

    def set_section(self, s, name):
        """Sets the section label for the given bars.

        :param str s: A selection string
        :param str name: The name of the section label
        """
        self.app.sections.set(s, name)

    def set_material(self, s, name):
        """Sets the material label for the given bars.

        :param str s: A selection string
        :param str name: The name of the material label
        """
        self.app.materials.set(s, name)

    def set_release(self, s, name):
        """Sets the release label for the given bars.

        :param str s: A selection string
        :param str name: The name of the release label
        """
        self.app.releases.set(s, name)
