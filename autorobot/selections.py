from .constants import ROType

from .extensions import Capsule

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotSelectionFactory,
)

class ExtendedSelectionFactory(Capsule):
    """
    This class is an extension of ``IRobotSelectionFactory`` providing the
    mehtods listed below in addition to the methods of the original object.
    """

    _otype = IRobotSelectionFactory

    def clear_current(self):
        """Clears the current GUI selection of all objects."""
        for t in ROType:
            if t != ROType.UNDEFINED:
                self.Get(t).Clear()
