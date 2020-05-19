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
    '''Returns the distance between to nodes or arrays.
    
    :param int node, other: Nodes' numbers (both args can also be node objects or numpy arrays)
    :return: The distance between two nodes
    :rtype: float
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
