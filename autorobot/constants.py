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
    IRobotQuitOption,
)


class RProjType(IntEnum):
    '''Aliases for common project types (others exist, see ``IRobotProjectType``).'''
    
    BUILDING = IRobotProjectType.I_PT_BUILDING
    FRAME_2D = IRobotProjectType.I_PT_FRAME_2D
    FRAME_3D = IRobotProjectType.I_PT_FRAME_3D
    SHELL = IRobotProjectType.I_PT_SHELL
    TRUSS_2D = IRobotProjectType.I_PT_TRUSS_2D
    TRUSS_3D = IRobotProjectType.I_PT_TRUSS_3D
    

class RQuitOpt(IntEnum):
    '''Aliases for quit options (see ``IRobotQuitOption``).'''
    DISCARD = IRobotQuitOption.I_QO_DISCARD_CHANGES
    PROMPT = IRobotQuitOption.I_QO_PROMPT_TO_SAVE_CHANGES
    SAVE = IRobotQuitOption.I_QO_SAVE_CHANGES


class ROType:
    '''Aliases for object types (other exist see ``IRobotObjecttype``).'''

    BAR = IRobotObjectType.I_OT_BAR
    CASE = IRobotObjectType.I_OT_CASE
    NODE = IRobotObjectType.I_OT_NODE


class RCaseType(IntEnum):
    '''Aliases for case type (see ``IRobotCaseType``).'''

    SIMPLE = IRobotCaseType.I_CT_SIMPLE
    COMB = IRobotCaseType.I_CT_COMBINATION

    
class RLoadType:
    '''Aliases for load record types (see ``IRobotLoadRecordType``).'''

    DEAD = IRobotLoadRecordType.I_LRT_DEAD
    NODAL = IRobotLoadRecordType.I_LRT_NODE_FORCE
    BAR_UDL = IRobotLoadRecordType.I_LRT_BAR_UNIFORM
    BAR_PL = IRobotLoadRecordType.I_LRT_BAR_FORCE_CONCENTRATED


class RBarUDLValues:
    '''Aliases for bars' uniform distributed loads (see ``IRobotBarUniformRecordValues``).'''

    FX = IRobotBarUniformRecordValues.I_BURV_PX
    FY = IRobotBarUniformRecordValues.I_BURV_PY
    FZ = IRobotBarUniformRecordValues.I_BURV_PZ
    ALPHA = IRobotBarUniformRecordValues.I_BURV_ALPHA
    BETA = IRobotBarUniformRecordValues.I_BURV_BETA
    GAMMA = IRobotBarUniformRecordValues.I_BURV_GAMMA
    IS_LOC = IRobotBarUniformRecordValues.I_BURV_LOCAL
    IS_PROJ = IRobotBarUniformRecordValues.I_BURV_PROJECTION
    IS_REL = IRobotBarUniformRecordValues.I_BURV_RELATIVE
    OFFSET_Y = IRobotBarUniformRecordValues.I_BURV_OFFSET_Y
    OFFSET_Z = IRobotBarUniformRecordValues.I_BURV_OFFSET_Z


class RBarPLValues:
    '''Aliases for bars' point loads (see ``IRobotBarForceConcentrateRecordValues``).'''

    X = IRobotBarForceConcentrateRecordValues.I_BFCRV_X
    FX = IRobotBarForceConcentrateRecordValues.I_BFCRV_FX
    FY = IRobotBarForceConcentrateRecordValues.I_BFCRV_FY
    FZ = IRobotBarForceConcentrateRecordValues.I_BFCRV_FZ
    CX = IRobotBarForceConcentrateRecordValues.I_BFCRV_CX
    CY = IRobotBarForceConcentrateRecordValues.I_BFCRV_CY
    CZ = IRobotBarForceConcentrateRecordValues.I_BFCRV_CZ
    ALPHA = IRobotBarForceConcentrateRecordValues.I_BFCRV_ALPHA
    BETA = IRobotBarForceConcentrateRecordValues.I_BFCRV_BETA
    GAMMA = IRobotBarForceConcentrateRecordValues.I_BFCRV_GAMMA
    GEN_NODE = IRobotBarForceConcentrateRecordValues.I_BFCRV_GENERATE_CALC_NODE
    IS_LOC = IRobotBarForceConcentrateRecordValues.I_BFCRV_LOC
    IS_REL = IRobotBarForceConcentrateRecordValues.I_BFCRV_REL
    OFFSET_Y = IRobotBarForceConcentrateRecordValues.I_BFCRV_OFFSET_Y
    OFFSET_Z = IRobotBarForceConcentrateRecordValues.I_BFCRV_OFFSET_Z
