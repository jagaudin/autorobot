from collections.abc import Iterable
from itertools import repeat
import numpy as np
from scipy.spatial import distance as sci_distance

import autorobot.app as app
from .extensions import (
    Capsule,
    ExtendedServer,
)
from .constants import (
    ROType,
)
from .decorators import requires_init
from .errors import (
    AutoRobotIdError,
    AutoRobotValueError,
)

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotNode,
    IRobotNodeServer,
)


@requires_init
def distance(node, other):
    """Returns the distance between two nodes or arrays.

    :param int node, other: Nodes' numbers

    .. tip::

      The arguments **node** and **other** can also be
      :py:class:`.ExtendedNode`, ``IRobotNode``, ``str`` or
      a 1D ``numpy.ndarray``.
    """
    if not all((isinstance(n, np.ndarray) for n in (node, other))):
        try:
            node, other = (
                n if isinstance(n, ExtendedNode)
                else ExtendedNode(n) if isinstance(n, IRobotNode)
                else app.app.nodes.get(int(n))
                for n in (node, other)
            )
        except Exception as e:
            raise AutoRobotValueError(
                f"Couldn't get distance between {node} and {other}."
            ) from e
        node, other = (n.as_array() for n in (node, other))

    return sci_distance.euclidean(node, other)


class ExtendedNode(Capsule):
    """
    This class is an extension for ``IRobotNode`` providing the
    mehtods listed below in addition to the methods of the original object.
    """

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
        """
        return np.array([self.node.X, self.node.Y, self.node.Z])

    def dist_to(self, other):
        """Returns the distance between the node and another.

        :param int other:
            The number of the other node. See :py:func:`.distance`
            for more details.
        """
        return distance(self, other)

    def closest(self, s, count=1, obj=False):
        """Returns the n-closest nodes amongst a selection.

        :param str s: A valid selection string
        :param int count:
           Number of closest points. `-1` sorts the whole selection
           from closest to farthest
        :param bool obj:
           Whether the function returns objects, or just object numbers.
        :return:
            The unique closest node as an instance of
            :py:class:`.ExtendedNode`, its number or a n-list
            of nodes or numbers sorted from closest to farthest.
        """
        with app.app.nodes as nodes:
            coords = nodes.table(str(s))
            n = self.as_array()
            distances = (
                sci_distance.cdist(n[None, :], coords[:, -3:]).flatten())

            if count == 1:
                id_min = np.argmin(distances)
                node_num = coords[id_min, 0]
                return nodes.get(node_num) if obj else node_num

            if count == -1:
                res = coords[distances.argsort(), 0]
            else:
                res = coords[distances.argsort()[:count], 0]
            if obj:
                return [nodes.get(i) for i in res]
            else:
                return [int(i) for i in res]


class ExtendedNodeServer(ExtendedServer):
    """
    This class is an extension for ``IRobotNodeServer`` providing
    additional functions for the management of nodes.
    """

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

    def table(self, s):
        """Returns a 2d array with the nodes numbers and coordinates.

        The returned array has four columns containing respectively the nodes'
        number, the x, y and z coordinates.

        :param str s: A valid selection string
        :return: A 2d array with the nodes numbers and coordinates
        """
        return np.stack(
            [np.array([n.Number, n.X, n.Y, n.Z]) for n in self.select(s)]
        )

    def from_array(self, a, num=None, obj=True, overwrite=False):
        """Returns a new node created from a coordinate array.

        If the array has one dimension the first three values are used as
        coordinates. If the array has two dimensions and three columns,
        the data is used as coordinates. If the array has two dimensions
        and more than three columns, the first columns is used as numbers
        for the newly created nodes (and the argument **num** is ignored).

        :param numpy.array a: An array-like object (1d or 2d)
        :param num: The new number(s) for the node(s) (optional)
        :type num: int or tuple
        :param bool obj:
           Whether to return the node object or its number (default: `True`)
        :param bool overwrite: Whether to overwrite existing objects
        :return: The new node object(s) or number(s)
        """
        a = np.asarray(a)
        if len(a.shape) == 1:
            return self.create(*a[:3], num=num, obj=obj, overwrite=overwrite)
        elif len(a.shape) > 2:
            raise AutoRobotValueError("Array must be 1d or 2d.")

        if a.shape[1] > 3:
            # Use first column as numbers and remove it
            num = iter(a[:, :1].flatten().astype(int))
            a = a[:, 1:]
        else:
            num = iter(num) if isinstance(num, Iterable) else repeat(None)
        new = []
        for row in a:
            new.append(self.create(*row[:3], num=next(num), obj=obj,
                                   overwrite=overwrite))
        return new

    def set_support(self, s, name):
        """Sets the support label for the given nodes.

        :param str s: A valid selection string
        :param str name: The name of the support label
        """
        self.app.supports.set(s, name)
