import numpy as np

import autorobot.app as app
from .constants import RLabelType

from .extensions import (
    ExtendedLabel,
    ExtendedLabelServer,
)
from .nodes import ExtendedNode
from .errors import AutoRobotValueError

from .robotom import RobotOM
from RobotOM import (
    IRobotLabel,
    IRobotLabelServer,
    IRobotNode,
    IRobotNodeSupportData,
    IRobotNodeSupportFixingDirection,
)

class ExtendedSupportLabel(ExtendedLabel):
    """
    This class is an extension for ``IRobotLabel`` providing new
    methods in addition to the methods of the original object.
    """

    _otype = IRobotLabel
    _dtype = IRobotNodeSupportData

    @property
    def UX(self):
        """
        Whether the X-direction degree of freedom is fixed
        (**True**) or free (**False**).
        """
        return self.data.UX

    @property
    def UY(self):
        """
        Whether the Y-direction degree of freedom is fixed
        (**True**) or free (**False**).
        """
        return self.data.UY

    @property
    def UZ(self):
        """
        Whether the Z-direction degree of freedom is fixed
        (**True**) or free (**False**).
        """
        return self.data.UZ

    @property
    def RX(self):
        """
        Whether the X-axis rotation degree of freedom is fixed
        (**True**) or free (**False**).
        """
        return self.data.RX

    @property
    def RY(self):
        """
        Whether the Y-axis rotation degree of freedom is fixed
        (**True**) or free (**False**).
        """
        return self.data.RY

    @property
    def RZ(self):
        """
        Whether the Z-axis rotation degree of freedom is fixed
        (**True**) or free (**False**).
        """
        return self.data.RZ


class ExtendedSupportServer(ExtendedLabelServer):
    """
    This class is an extension for ``IRobotLabelServer`` providing
    additional functions for the management of section labels.
    """

    _otype = IRobotLabelServer
    _ctype = IRobotLabel
    _ltype = RLabelType.SUPPORT
    _dtype = IRobotNodeSupportData
    _rtype = ExtendedSupportLabel

    def create(self, name, dof, elasticity=None,
               alpha=0., beta=0., gamma=0., node=None, orient_node=None,
               unit_force=1e3, unit_angle=np.pi / 180):
        """Creates a support oriented towards a point.

        :param str name:
           The name of the support. It will be suffixed with the
           node number if `n` refers to a selection.
        :param str dof:
           The degree of freedom at the support. Falsy values are
           free (`dof` can be a string like `111000` for a pin)
        :param tuple elasticity:
           Values representing the elasticity of the support for
           all degree of freedom
        :param float alpha, beta, gamma: Orientation angles
        :param int node, orient_node:
           The nodes defining the orientation of the support.

           .. note:
              If **orient_node** is specified, then the values of
              the angles **alpha**, **beta**, **gamma** will be
              ignored.

        :param float unit_force:
           The factor to apply to elastic force (default is 1e3 so that
           input is in kN)
        :param float unit_angle:
           The factor to apply to angle values (default is π / 180 so
           that input is in degree)
        """
        dof = {
            'I_NSFD_UX': bool(int(dof[0])),
            'I_NSFD_UY': bool(int(dof[1])),
            'I_NSFD_UZ': bool(int(dof[2])),
            'I_NSFD_RX': bool(int(dof[3])),
            'I_NSFD_RY': bool(int(dof[4])),
            'I_NSFD_RZ': bool(int(dof[5])),
        }

        label = self._ctype(self.Create(self._ltype, name))
        data = self._dtype(label.Data)

        for prop, val in dof.items():
            data.SetFixed(
                getattr(IRobotNodeSupportFixingDirection, prop), bool(val)
            )

        if elasticity is not None:
            params = {
                'KX': elasticity[0] * unit_force,
                'KY': elasticity[1] * unit_force,
                'KZ': elasticity[2] * unit_force,
                'HX': elasticity[3] * unit_force / unit_angle,
                'HY': elasticity[4] * unit_force / unit_angle,
                'HZ': elasticity[5] * unit_force / unit_angle,
            }
            for prop, val in params.items():
                setattr(data, prop, val)
        else:
            for prop in ['KX', 'KY', 'KZ', 'HX', 'HY', 'HZ']:
                setattr(data, prop, 0.)

        if orient_node is None:
            data.Alpha = alpha * unit_angle
            data.Beta = beta * unit_angle
            data.Gamma = gamma * unit_angle
        else:
            if not all((isinstance(orient_node, np.ndarray)
                        for n in (node, orient_node))):
                try:
                    node, orient_node = (
                        n if isinstance(n, ExtendedNode)
                        else ExtendedNode(n) if isinstance(n, IRobotNode)
                        else app.app.nodes.get(int(n))
                        for n in (node, orient_node)
                    )
                except Exception as e:
                    raise AutoRobotValueError(
                        f"Couldn't read {node} and/or {orient_node}."
                    ) from e
                node, orient_node = (n.as_array() for n in (node, orient_node))

            v = orient_node - node
            v_norm = v / (np.linalg.norm(v) + 1e-16)

            data.Alpha = np.arctan2(v_norm[1], v_norm[0])
            data.Beta = np.arccos(v_norm[2])
            data.Gamma = 0.

        self.StoreWithName(label, name)
