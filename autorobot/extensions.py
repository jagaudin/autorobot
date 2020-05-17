from .constants import (
    _robot_dll_path,
    RCaseType,
)

from .errors import RobotNewProjError

import clr
clr.AddReference(_robot_dll_path)

from RobotOM import (
    IRobotBar,
    IRobotCase,
    IRobotCaseCombination,
    IRobotNode,
    IRobotSimpleCase,
    RobotApplication,
)


class ExtendedRobotApp:
    def __init__(self):
        self.app = RobotApplication()
    
    @property
    def bars(self):
        return ExtendedBarServer(self.app.Project.Structure.Bars)
    
    @property
    def cases(self):
        return ExtendedCaseServer(self.app.Project.Structure.Cases)
    
    @property
    def nodes(self):
        return ExtendedNodeServer(self.app.Project.Structure.Nodes)
    
    @property
    def structure(self):
        return self.app.Project.Structure
    
    def open(self, path):
        self.app.Project.Open(path)
        
    def new(self, proj_type):
        try:
            self.app.Project.New(proj_type)
        except Exception as e:
            raise(RobotNewProjError, f"Couldn't create new project with '{proj_type}'.")
        
    def show(self, interactive=True):
        self.app.Visible = True
        self.app.Interactive = interactive
        
    def hide(self):
        self.app.Visible = False

    def __getattr__(self, name):
        if hasattr(self.app, name):
            return getattr(self.app, name)
        raise AttributeError(f"{self.__class__.__name__} has not attribute '{name}'.")


class ExtendedBarServer:
    def __init__(self, inst):
        self.server = inst
        
    def get(self, n):
        return IRobotBar(self.server.Get(n))
    
    def __getattr__(self, name):
        if hasattr(self.server, name):
            return getattr(self.server, name)
        raise AttributeError(f"{self.__class__.__name__} has not attribute '{name}'.")
        
        
class ExtendedCaseServer:
    def __init__(self, inst):
        self.server = inst
        
    def get(self, n):
        c = IRobotCase(self.server.Get(n))
        if c.Type == RCaseType.SIMPLE:
            return IRobotSimpleCase(c)
        elif c.Type == RCaseType.COMB:
            return IRobotCaseCombination(c)
    
    def __getattr__(self, name):
        if hasattr(self.server, name):
            return getattr(self.server, name)
        raise AttributeError(f"{self.__class__.__name__} has not attribute '{name}'.")

        
class ExtendedNodeServer:
    def __init__(self, inst):
        self.server = inst
        
    def get(self, n):
        return IRobotNode(self.server.Get(n))
    
    def __getattr__(self, name):
        if hasattr(self.server, name):
            return getattr(self.server, name)
        raise AttributeError(f"{self.__class__.__name__} has not attribute '{name}'.")
        
        



rb = ExtendedRobotApp()

