import clr
from pathlib import Path
from enum import IntEnum

from .errors import RobotPathError

# Searching for ``interop.RobotOM.dll``
p = Path(r'C:\Program Files\Autodesk')
suffix = r'System\EXE\interop.RobotOM.dll'

_robot_dll_path = str(next(p.rglob(suffix), ''))

try:
    clr.AddReference(_robot_dll_path)
except Exception as e:
    raise(RobotPathError(f"Couldn't find {p}\\*\\{suffix}"))

from RobotOM import (
    IRobotCaseType,
    IRobotProjectType,
)


class RProjType(IntEnum):
    '''Aliases for common project types (others exist, see ``IRobotProjectType``).'''
    #: ``IRobotProjectType.I_PT_BUILDING``
    BUILDING = IRobotProjectType.I_PT_BUILDING
    #: ``IRobotProjectType.I_PT_FRAME_2D``
    FRAME_2D = IRobotProjectType.I_PT_FRAME_2D
    #: ``IRobotProjectType.I_PT_FRAME_3D``
    FRAME_3D = IRobotProjectType.I_PT_FRAME_3D
    #: ``IRobotProjectType.I_PT_SHELL``   
    SHELL = IRobotProjectType.I_PT_SHELL
    #: ``IRobotProjectType.I_PT_TRUSS_2D``
    TRUSS_2D = IRobotProjectType.I_PT_TRUSS_2D
    #: ``IRobotProjectType.I_PT_TRUSS_3D``
    TRUSS_3D = IRobotProjectType.I_PT_TRUSS_3D


class RCaseType(IntEnum):
    '''Aliases for case type (see ``IRobotCaseType``).'''
    #: ``IRobotCaseType.I_CT_SIMPLE``
    SIMPLE = IRobotCaseType.I_CT_SIMPLE
    #: ``IRobotCaseType.I_CT_COMBINATION``
    COMB = IRobotCaseType.I_CT_COMBINATION
