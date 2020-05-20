import numpy as np
from scipy.spatial import distance as sci_distance

import autorobot.extensions as extensions
from .extensions import ExtendedNode
from .constants import _robot_dll_path
from .decorators import requires_init
from .errors import AutoRobotValueError

import clr
clr.AddReference(_robot_dll_path)
from RobotOM import IRobotNode
    

@requires_init
def distance(node, other):
    '''Returns the distance between two nodes or arrays.
    
    :param int node, other: Nodes' numbers
    
    .. tip:: The arguments **node** and **other** can also be :py:class:`.ExtendedNode`, ``IRobotNode`` or ``str``.
    '''
    if not all((isinstance(n, np.ndarray) for n in (node, other))):
        try:
            node, other = (
                n if isinstance(n, ExtendedNode)
                else ExtendedNode(n) if isinstance(n, IRobotNode) 
                else extensions.app.nodes.get(int(n)) 
                for n in (node, other)
            )
        except Exception as e:
            raise AutoRobotValueError(
                f"Couldn't get distance between {node} and {other}."
            ) from e
        node, other = (n.to_array() for n in (node, other))
        
    return sci_distance.euclidean(node, other)
