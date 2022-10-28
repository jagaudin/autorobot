from .constants import (
    RLabelType,
    ROType,
    RReleaseValues,
)
from .decorators import accepts_name_as_attribute

from .extensions import (
    ExtendedLabel,
    ExtendedLabelServer,
)

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotBarEndReleaseData,
    IRobotBarReleaseData,
    IRobotLabel,
    IRobotLabelServer,
)


class ExtendedReleaseLabel(ExtendedLabel):
    """
    This class is an extension for ``IRobotLabel`` providing new
    methods in addition to the methods of the original object.
    """

    _otype = IRobotLabel
    _dtype = IRobotBarReleaseData

    @property
    def start(self):
        """Start node release."""
        return self.data.StartNode

    @property
    def end(self):
        """End node release."""
        return self.data.EndNode


class ExtendedReleaseServer(ExtendedLabelServer):
    """
    This class is an extension for ``IRobotLabelServer`` providing
    additional functions for the management of bar release labels.
    """

    _otype = IRobotLabelServer
    _ctype = IRobotLabel
    _ltype = RLabelType.RELEASE
    _dtype = IRobotBarReleaseData
    _rtype = ExtendedReleaseLabel

    def create(self, name, start, end):
        """Creates a label defining bar end releases.

        :param str name: The name of the release
        :param str start, end:
            The releases at each end of the bar. Falsy values are
            free (`start` and `end` can be a string like `111000`
            for a pin)
        """
        input = [
            {
                "UX": RReleaseValues(int(start[0])),
                "UY": RReleaseValues(int(start[1])),
                "UZ": RReleaseValues(int(start[2])),
                "RX": RReleaseValues(int(start[3])),
                "RY": RReleaseValues(int(start[4])),
                "RZ": RReleaseValues(int(start[5])),
            },
            {
                "UX": RReleaseValues(int(end[0])),
                "UY": RReleaseValues(int(end[1])),
                "UZ": RReleaseValues(int(end[2])),
                "RX": RReleaseValues(int(end[3])),
                "RY": RReleaseValues(int(end[4])),
                "RZ": RReleaseValues(int(end[5])),
            },
        ]

        label = self._ctype(self.Create(self._ltype, name))
        data = self._dtype(label.Data)
        node_data = [
            IRobotBarEndReleaseData(data.StartNode),
            IRobotBarEndReleaseData(data.EndNode),
        ]

        for data, params in zip(node_data, input):
            for dof, val in params.items():
                setattr(data, dof, val)

        self.StoreWithName(label, name)
        return self.get(name)

    @accepts_name_as_attribute
    def set(self, name, s):
        """Sets the releases for a selection of bars.

        :param str name: The release label name
        :param str s: A valid selection string
        """
        sel = self._app.selections.Create(ROType.BAR)
        sel.FromText(str(s))
        with self._app.bars as bars:
            bars.SetLabel(sel, self._ltype, str(name))
