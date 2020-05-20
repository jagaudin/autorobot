import clr
from pathlib import Path
from enum import IntEnum

from .errors import AutoRobotPathError

# Searching for ``interop.RobotOM.dll``
p = Path(r'C:\Program Files\Autodesk')
suffix = r'System\EXE\interop.RobotOM.dll'

_robot_dll_path = str(next(p.rglob(suffix), ''))

try:
    clr.AddReference(_robot_dll_path)
except Exception as e:
    raise(AutoRobotPathError(f"Couldn't find {p}\\*\\{suffix}")) from e

from RobotOM import (
    IRobotBarForceConcentrateRecordValues,
    IRobotBarUniformRecordValues,
    IRobotCaseType,
    IRobotLoadRecordType,
    IRobotObjectType,
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

    
class ROType:
    '''Aliases for object types (other exist see ``IRobotObjecttype``).'''
    
    BAR = IRobotObjectType.I_OT_BAR
    CASE = IRobotObjectType.I_OT_CASE
    NODE = IRobotObjectType.I_OT_NODE

    
class RCaseType(IntEnum):
    '''Aliases for case type (see ``IRobotCaseType``).'''
    #: ``IRobotCaseType.I_CT_SIMPLE``
    SIMPLE = IRobotCaseType.I_CT_SIMPLE
    #: ``IRobotCaseType.I_CT_COMBINATION``
    COMB = IRobotCaseType.I_CT_COMBINATION


class RBarUDLValues:
    '''Aliases for bars' uniform distributed loads (see ``IRobotBarUniformRecordValues``).'''
    #: ``IRobotBarUniformRecordValues.I_BURV_PX``
    FX = IRobotBarUniformRecordValues.I_BURV_PX
    #: ``IRobotBarUniformRecordValues.I_BURV_PY``
    FY = IRobotBarUniformRecordValues.I_BURV_PY
    #: ``IRobotBarUniformRecordValues.I_BURV_PZ``
    FZ = IRobotBarUniformRecordValues.I_BURV_PZ
    #: ``IRobotBarUniformRecordValues.I_BURV_ALPHA``
    ALPHA = IRobotBarUniformRecordValues.I_BURV_ALPHA
    #: ``IRobotBarUniformRecordValues.I_BURV_BETA``
    BETA = IRobotBarUniformRecordValues.I_BURV_BETA
    #: ``IRobotBarUniformRecordValues.I_BURV_GAMMA``
    GAMMA = IRobotBarUniformRecordValues.I_BURV_GAMMA
    #: ``IRobotBarUniformRecordValues.I_BURV_LOCAL``
    IS_LOC = IRobotBarUniformRecordValues.I_BURV_LOCAL
    #: ``IRobotBarUniformRecordValues.I_BURV_PROJECTION``
    IS_PROJ = IRobotBarUniformRecordValues.I_BURV_PROJECTION
    #: ``IRobotBarUniformRecordValues.I_BURV_RELATIVE``
    IS_REL = IRobotBarUniformRecordValues.I_BURV_RELATIVE
    #: ``IRobotBarUniformRecordValues.I_BURV_OFFSET_Y``
    OFFSET_Y = IRobotBarUniformRecordValues.I_BURV_OFFSET_Y
    #: ``IRobotBarUniformRecordValues.I_BURV_OFFSET_Z``
    OFFSET_Z = IRobotBarUniformRecordValues.I_BURV_OFFSET_Z
    
    
class RBarPLValues:
    '''Aliases for bars' point loads (see ``IRobotBarForceConcentrateRecordValues``).'''
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_X``
    X = IRobotBarForceConcentrateRecordValues.I_BFCRV_X
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_FX``
    FX = IRobotBarForceConcentrateRecordValues.I_BFCRV_FX
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_FY``
    FY = IRobotBarForceConcentrateRecordValues.I_BFCRV_FY
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_FZ``
    FZ = IRobotBarForceConcentrateRecordValues.I_BFCRV_FZ
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_CX``
    CX = IRobotBarForceConcentrateRecordValues.I_BFCRV_CX
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_CY``
    CY = IRobotBarForceConcentrateRecordValues.I_BFCRV_CY
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_CZ``
    CZ = IRobotBarForceConcentrateRecordValues.I_BFCRV_CZ
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_ALPHA``
    ALPHA = IRobotBarForceConcentrateRecordValues.I_BFCRV_ALPHA
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_BETA``
    BETA = IRobotBarForceConcentrateRecordValues.I_BFCRV_BETA
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_GAMMA``
    GAMMA = IRobotBarForceConcentrateRecordValues.I_BFCRV_GAMMA
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_GENERATE_CALC_NODE``
    GEN_NODE = IRobotBarForceConcentrateRecordValues.I_BFCRV_GENERATE_CALC_NODE
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_LOC``
    IS_LOC = IRobotBarForceConcentrateRecordValues.I_BFCRV_LOC
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_REL``
    IS_REL = IRobotBarForceConcentrateRecordValues.I_BFCRV_REL
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_OFFSET_Y``
    OFFSET_Y = IRobotBarForceConcentrateRecordValues.I_BFCRV_OFFSET_Y
    #: ``IRobotBarForceConcentrateRecordValues.I_BFCRV_OFFSET_Z``
    OFFSET_Z = IRobotBarForceConcentrateRecordValues.I_BFCRV_OFFSET_Z

    
class RLoadType:
    #: ``IRobotLoadRecordType.I_LRT_DEAD``
    DEAD = IRobotLoadRecordType.I_LRT_DEAD
    #: ``IRobotLoadRecordType.I_LRT_NODE_FORCE``
    NODAL = IRobotLoadRecordType.I_LRT_NODE_FORCE
    #: ``IRobotLoadRecordType.I_LRT_BAR_UNIFORM``
    BAR_UDL = IRobotLoadRecordType.I_LRT_BAR_UNIFORM
    #: ``IRobotLoadRecordType.I_LRT_BAR_FORCE_CONCENTRATED``
    BAR_PL = IRobotLoadRecordType.I_LRT_BAR_FORCE_CONCENTRATED
