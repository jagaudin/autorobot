import sys
from abc import ABC
import numpy as np


from .constants import (
    _robot_dll_path,
    RCaseType,
    ROType,
)
from .decorators import abstract_attributes
from .errors import (
    AutoRobotProjError,
    AutoRobotValueError,
)

import clr
clr.AddReference(_robot_dll_path)

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
    '''This class encapsulates and extends ``RobotApplication``. 
    The attributes and methods of the underlying ``RobotApplication`` object can be accessed directly through an instance of this class
    
    :param bool visible: Whether the new ``RobotApplication`` is visible (default: ``True``)
    :param bool interactive: Whether the new ``RobotApplication`` is interactive (default: ``True``)
    '''
    def __init__(self, visible=True, interactive=True):
        '''Constructor method
        '''
        self.app = RobotApplication()
        if visible:
            self.show(interactive)
    
    @property
    def bars(self):
        '''Gets the current project's bar server as an instance of :py:class:`.ExtendedBarServer`.
        '''
        return ExtendedBarServer(self.app.Project.Structure.Bars, self)
    
    @property
    def cases(self):
        '''Gets the current project's case server as an instance of :py:class:`.ExtendedCaseServer`.
        '''
        return ExtendedCaseServer(self.app.Project.Structure.Cases, self)
    
    @property
    def nodes(self):
        '''Gets the current project's node server as an instance of :py:class:`.ExtendedNodeServer`.
        '''
        return ExtendedNodeServer(self.app.Project.Structure.Nodes, self)
    
    @property
    def select(self):
        return ExtendedSelectionFactory(self.app.Project.Structure.Selections)
    
    @property
    def structure(self):
        '''Get the current object structure as an instance of ``IRobotStructure``.
        '''
        return self.app.Project.Structure
    
    def open(self, path):
        '''Opens a file with given path.
        
        :param path: The path to the file
        :type param: str or pathlib.Path
        '''
        self.app.Project.Open(str(path))
        
    def new(self, proj_type):
        '''Creates a new project.
        
        :param int proj_type: The type of project to be created (see :py:class:`.constants.RProjType`)
        '''
        try:
            self.app.Project.New(proj_type)
        except Exception as e:
            raise AutoRobotProjError(
                f"Couldn't create new project with '{proj_type}'."
            )
        
    def show(self, interactive=True):
        '''Makes the ``RobotApplication`` visible.
        
        :param bool interactive: Whether the ``RobotApplication`` is interactive (default: ``True``)
        '''
        self.app.Visible = True
        self.app.Interactive = interactive
        
    def hide(self):
        '''Hides the ``RobotApplication``.
        '''
        self.app.Visible = False

    def __getattr__(self, name):
        if hasattr(self.app, name):
            return getattr(self.app, name)
        raise AttributeError(f"{self.__class__.__name__} has not attribute '{name}'.")

        
@abstract_attributes('_otype')     
class Capsule(ABC):
    def __init__(self, inst):
        self._inst = inst
        if not isinstance(inst, self._otype):
            raise AutoRobotValueError(f"{inst} is not an instance of `{str(self._otype)}`.")
        
    def __getattr__(self, name):
        if hasattr(self._inst, name):
            return getattr(self._inst, name)
        raise AttributeError(f"{self.__class__.__name__} has not attribute '{name}'.")

        
class ExtendedNode(Capsule):
    
    _otype = IRobotNode
    
    def __init__(self, inst):
        '''Constructor method.'''
        
        super(ExtendedNode, self).__init__(inst)
        self.node = inst
    
    def to_array(self):
        '''Returns an array with the node's coordinates.
    
        :return: A numpy array of coordinates
        :rtype: numpy array
        ''' 
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

    def __exit__(self, exc_type,exc_value, traceback):
        if hasattr(self.server, 'EndMultiOperation'):
            self.server.EndMultiOPeration()
            
    def get(self, n):
        '''Returns the object with id number `n` from the server.
        
        :param int n: The object's number
        
        .. note:: The function casts the argument **n** to ``int`` before querying the server. 
        '''
        try:
            return self._rtype(self._ctype(self.server.Get(int(n))))
        except Exception as e:
            raise AutoRobotValueError(
                f"{self.__class__.__name__} couldn't get id `{n}`."
            ) from e
            
    def select(self, s, obj=True):
        '''Returns an iterator of objects referred to by numbers in a selection string.
        
        :param str s: A valid selection string
        :param bool obj: Whether to return the objects or their numbers.
        :return: A generator of the selected objects
        '''
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
     
    def create(self, start, end, num=None, obj=True):
        '''Creates a new bar between ``start`` and ``end`` nodes.

        :param start, end: The start and end nodes
        :type start, end: IRobotNode or int
        :param int num: The number of the new bar (optional)
        :param bool obj: Whether the bar is returned as an object (default: ``True``)
        :return: The new bar or its number
        :rtype: IRobotBar or int
        '''
        try:
            start, end = (
                n.Number if hasattr(n, 'Number') else int(n) for n in (start, end)
            )
        except Exception as e:
            raise AutoRobotValueError(
                f"Couldn't create bar with nodes `{start}` and `{end}`."
            ) from e
        if num is None:
            num = self.FreeNumber
        self.Create(num, start, end)
        return self.get(num) if obj else num
    
        
class ExtendedCaseServer(ExtendedServer):
    
    _otype = IRobotCaseServer
    _ctype = IRobotCase
    _dtype = ROType.CASE
    _rtype = IRobotCase
    
    @staticmethod
    def cast(case):
        '''Recasts a load case object according to its type.
        
        :param IRobotCase case: The load case object
        '''
        if case.Type == RCaseType.SIMPLE:
            return IRobotSimpleCase(case)
        elif case.Type == RCaseType.COMB:
            return IRobotCaseCombination(case)
        
    def get(self, n):
        '''A method to retrieve load case objects from the server.
        
        :param int n: The case number
        
        .. note:: The function casts the argument **n** to ``int`` before querying the server. 
        '''
        return self.cast(super(ExtendedCaseServer, self).get(n))
        
        
    def select(self, s, obj=True):
        '''Returns an iterator of load case objects referred to in a selection string.
        
        :param str s: A valid selection string
        :param bool obj: Whether to return case objects or cases' numbers
        :return: A generator of the selected load cases
        '''
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
    
    def create(self, x, y, z, num=None, obj=True):
        '''Creates a new node from coordinates.
        
        :param float x, y, z: Coordinates of the new node
        :param int num: The number for the new node
        :param bool obj: Whether to return the node object or its number
        :return: The new node object (as :py:class:`ExtendedNode`) or its number (as ``int``)
        '''
        num = num or self.FreeNumber
        self.Create(num, float(x), float(y), float(z))
        return self.get(num) if obj else num
               

class ExtendedSelectionFactory(Capsule):
    _otype = IRobotSelectionFactory
   
        
def initialize(visible=True, interactive=True):
    '''Initialize a ``RobotApplication`` object.
    
    :param bool visible: Whether the application window is displayed
    :param bool interactive: Whether the application window is displayed
    
    .. note:: A reference to the ``RobotApplication`` is stored in :py:data:`autorobot.extensions.app`.
    '''
    _this.app = ExtendedRobotApp(visible, interactive)
    return _this.app

#: A reference to the current ``RobotApplication`` instance
app = None