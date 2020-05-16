from .constants import (
    _robot_dll_path,
)

from .errors import RobotNewProjError

import types

import clr
clr.AddReference(_robot_dll_path)
from RobotOM import (
    RobotApplication,
)

rba = RobotApplication()



class ExtendedNodeServer:
    def __init__(self, inst):
        self.server = inst
        print('Hi')
    
    def get(self):
        pass
    
    def __getattr__(self, name):
        if hasattr(self.server, name):
            return getattr(self.server, name)
        raise AttributeError(f"{self.__class__.__name__} has not attribute '{name}'.") 

def _open_project(path):
    rba.Project.Open()

def _new_project(proj_type):
    try:
        rba.Project.New(proj_type)
    except Exception as e:
        raise(RobotNewProjError, f"Couldn't create new project with '{proj_type}'.")
    bars = rba.Project.Structure.Bars()
    
def extend_app():
    pass
    
def extend_bars(bars):
        
    pass

def extend_nodes():
    pass



nodes = rba.Project.Structure.Nodes
bars = rba.Project.Structure.Bars