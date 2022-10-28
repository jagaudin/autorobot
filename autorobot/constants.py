from enum import IntEnum

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotBarEndReleaseValue,
    IRobotBarForceConcentrateRecordValues,
    IRobotBarUniformRecordValues,
    IRobotCaseAnalizeType,
    IRobotCaseNature,
    IRobotCaseType,
    IRobotCombinationType,
    IRobotDeadRecordValues,
    IRobotLabelType,
    IRobotLicenseEntitlement,
    IRobotLicenseEntitlementStatus,
    IRobotLoadRecordType,
    IRobotMaterialType,
    IRobotObjectType,
    IRobotProjectType,
    IRobotQuitOption,
    IRobotTranslateOptions,
)


class RProjType(IntEnum):
    """
    Aliases for common project types. For more details, see
    ``IRobotProjectType``.
    """
    BUILDING = IRobotProjectType.I_PT_BUILDING
    FRAME_2D = IRobotProjectType.I_PT_FRAME_2D
    FRAME_3D = IRobotProjectType.I_PT_FRAME_3D
    SHELL = IRobotProjectType.I_PT_SHELL
    TRUSS_2D = IRobotProjectType.I_PT_TRUSS_2D
    TRUSS_3D = IRobotProjectType.I_PT_TRUSS_3D


class RQuitOpt(IntEnum):
    """
    Aliases for quit options. For more details, see ``IRobotQuitOption``.
    """
    DISCARD = IRobotQuitOption.I_QO_DISCARD_CHANGES
    PROMPT = IRobotQuitOption.I_QO_PROMPT_TO_SAVE_CHANGES
    SAVE = IRobotQuitOption.I_QO_SAVE_CHANGES


class ROType(IntEnum):
    """
    Aliases for object types. For more details, see ``IRobotObjectType``.
    """
    BAR = IRobotObjectType.I_OT_BAR
    CASE = IRobotObjectType.I_OT_CASE
    FE = IRobotObjectType.I_OT_FINITE_ELEMENT
    GEOMETRY = IRobotObjectType.I_OT_GEOMETRY
    GROUP = IRobotObjectType.I_OT_FAMILY
    NODE = IRobotObjectType.I_OT_NODE
    OBJECT = IRobotObjectType.I_OT_OBJECT
    PANEL = IRobotObjectType.I_OT_PANEL
    UNDEFINED = IRobotObjectType.I_OT_UNDEFINED
    VOLUME = IRobotObjectType.I_OT_VOLUME


class RLabelType:
    """
    Aliases for label types. For more details, see ``IRobotLabelType``.
    """
    BAR_SECT = IRobotLabelType.I_LT_BAR_SECTION
    MAT = IRobotLabelType.I_LT_MATERIAL
    SUPPORT = IRobotLabelType.I_LT_SUPPORT
    RELEASE = IRobotLabelType.I_LT_BAR_RELEASE


class RCaseNature(IntEnum):
    """
    Aliases for load case case nature. For more details, see
    ``IRobotCaseNature``.
    """
    PERM = IRobotCaseNature.I_CN_PERMANENT
    IMPOSED = IRobotCaseNature.I_CN_EXPLOATATION
    WIND = IRobotCaseNature.I_CN_WIND
    SNOW = IRobotCaseNature.I_CN_SNOW
    ACC = IRobotCaseNature.I_CN_ACCIDENTAL


class RCaseType(IntEnum):
    """
    Aliases for case type. For more details, see ``IRobotCaseType``.
    """
    SIMPLE = IRobotCaseType.I_CT_SIMPLE
    COMB = IRobotCaseType.I_CT_COMBINATION


class RCombType(IntEnum):
    """
    Aliases for load combination type. For more details, see
    ``IRobotCombinationType``.
    """
    SLS = IRobotCombinationType.I_CBT_SLS
    ULS = IRobotCombinationType.I_CBT_ULS


class RAnalysisType(IntEnum):
    """
    Aliases for analysis type. For more details, see
    ``IRobotCaseAnalizeType``.

    .. caution:: The typo is **in Robot API**, not this document.
    """
    LINEAR = IRobotCaseAnalizeType.I_CAT_STATIC_LINEAR
    NON_LIN = IRobotCaseAnalizeType.I_CAT_STATIC_NONLINEAR
    COMB_LINEAR = IRobotCaseAnalizeType.I_CAT_COMB
    COMB_NON_LIN = IRobotCaseAnalizeType.I_CAT_COMB_NONLINEAR


class RLoadType(IntEnum):
    """
    Aliases for load record types. For more details, see
    ``IRobotLoadRecordType``.
    """
    DEAD = IRobotLoadRecordType.I_LRT_DEAD
    NODAL = IRobotLoadRecordType.I_LRT_NODE_FORCE
    BAR_UDL = IRobotLoadRecordType.I_LRT_BAR_UNIFORM
    BAR_PL = IRobotLoadRecordType.I_LRT_BAR_FORCE_CONCENTRATED


class RMatType(IntEnum):
    """
    Aliases for material type. For more details, see
    ``IRobotMaterialType``.
    """
    STEEL = IRobotMaterialType.I_MT_STEEL
    ALUM = IRobotMaterialType.I_MT_ALUMINIUM
    TIMBER = IRobotMaterialType.I_MT_TIMBER
    CONCRETE = IRobotMaterialType.I_MT_CONCRETE
    OTHER = IRobotMaterialType.I_MT_OTHER


class RReleaseValues(IntEnum):
    """
    Aliases for bar end releases' values. For more details, see
    ``IRobotBarEndReleaseValue``.
    """
    NONE = IRobotBarEndReleaseValue.I_BERV_NONE
    STD = IRobotBarEndReleaseValue.I_BERV_STD
    FIXED = IRobotBarEndReleaseValue.I_BERV_FIXED


class RDeadValues(IntEnum):
    """
    Aliases for dead loads values. For more details, see
    ``IRobotDeadRecordValues``.
    """
    X = IRobotDeadRecordValues.I_DRV_X
    Y = IRobotDeadRecordValues.I_DRV_Y
    Z = IRobotDeadRecordValues.I_DRV_Z
    COEFF = IRobotDeadRecordValues.I_DRV_COEFF
    ENTIRE_STRUCT = IRobotDeadRecordValues.I_DRV_ENTIRE_STRUCTURE


class RBarUDLValues(IntEnum):
    """
    Aliases for bars' uniform distributed loads. For more details, see
    ``IRobotBarUniformRecordValues``.
    """
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


class RBarPLValues(IntEnum):
    """
    Aliases for bars' point loads. For more details, see
    ``IRobotBarForceConcentrateRecordValues``.
    """
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


class REditOpt(IntEnum):
    """
    Aliases for edit options. For more details, see ``IRobotTranslateOptions``.
    """
    COPY = IRobotTranslateOptions.I_TO_COPY
    MOVE = IRobotTranslateOptions.I_TO_MOVE


class RLicense(IntEnum):
    """
    Aliases for license entitlement. For more details see
    ``IRobotLicenseEntitlement``.
    """
    LOCAL = IRobotLicenseEntitlement.I_LE_LOCAL_SOLVE
    CLOUD = IRobotLicenseEntitlement.I_LE_CLOUD_SOLVE


class RLicenseStatus(IntEnum):
    """
    Aliases for license status. For more details see
    ``IRobotLicenseEntitlementStaus``
    """
    OK = IRobotLicenseEntitlementStatus.I_LES_ENTITLED
