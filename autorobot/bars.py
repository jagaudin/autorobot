import numpy as np

from .constants import (
    ROType,
)

from .extensions import (
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
)


class ExtendedBarServer(ExtendedServer):
    """
    This class is an extension for ``IRobotBarServer`` providing
    additional functions for the management of bars.
    """

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
