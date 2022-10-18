from .extensions import EnumCapsule

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
)


__all__ = [
    'RAnalysisType',
    'RBarPLValues',
    'RBarUDLValues',
    'RCaseNature',
    'RCaseType',
    'RCombType',
    'RDeadValues',
    'RLabelType',
    'RLicense',
    'RLicenseStatus',
    'RLoadType',
    'RMatType',
    'ROType',
    'RProjType',
    'RQuitOpt',
    'RReleaseValues',
]


RProjType = EnumCapsule(
    IRobotProjectType,
    {
        'BUILDING': 'I_PT_BUILDING',
        'FRAME_2D': 'I_PT_FRAME_2D',
        'FRAME_3D': 'I_PT_FRAME_3D',
        'SHELL': 'I_PT_SHELL',
        'TRUSS_2D': 'I_PT_TRUSS_2D',
        'TRUSS_3D': 'I_PT_TRUSS_3D'
    }
)
"""
Aliases for common project types. For more details, see
``IRobotProjectType``.
"""


RQuitOpt = EnumCapsule(
    IRobotQuitOption,
    {
        'DISCARD': 'I_QO_DISCARD_CHANGES',
        'PROMPT': 'I_QO_PROMPT_TO_SAVE_CHANGES',
        'SAVE': 'I_QO_SAVE_CHANGES'
    }
)
"""
Aliases for quit options. For more details, see ``IRobotQuitOption``.
"""


ROType = EnumCapsule(
    IRobotObjectType,
    {
        'BAR': 'I_OT_BAR',
        'CASE': 'I_OT_CASE',
        'NODE': 'I_OT_NODE'
    }
)
"""
Aliases for object types. For more details, see ``IRobotObjectType``.
"""


RLabelType = EnumCapsule(
    IRobotLabelType,
    {
        'BAR_SECT': 'I_LT_BAR_SECTION',
        'MAT': 'I_LT_MATERIAL',
        'SUPPORT': 'I_LT_SUPPORT',
        'RELEASE': 'I_LT_BAR_RELEASE'
    }
)
"""
Aliases for label types. For more details, see ``IRobotLabelType``.
"""


RCaseNature = EnumCapsule(
    IRobotCaseNature,
    {
        'PERM': 'I_CN_PERMANENT',
        'IMPOSED': 'I_CN_EXPLOATATION',
        'WIND': 'I_CN_WIND',
        'SNOW': 'I_CN_SNOW',
        'ACC': 'I_CN_ACCIDENTAL'
    }
)
"""
Aliases for load case case nature. For more details, see
``IRobotCaseNature``.
"""


RCaseType = EnumCapsule(
    IRobotCaseType,
    {
        'SIMPLE': 'I_CT_SIMPLE',
        'COMB': 'I_CT_COMBINATION'
    }
)
"""
Aliases for case type. For more details, see ``IRobotCaseType``.
"""


RCombType = EnumCapsule(
    IRobotCombinationType,
    {
        'SLS': 'I_CBT_SLS',
        'ULS': 'I_CBT_ULS'
    }
)
"""
Aliases for load combination type. For more details, see
``IRobotCombinationType``.
"""


RAnalysisType = EnumCapsule(
    IRobotCaseAnalizeType,
    {
        'LINEAR': 'I_CAT_STATIC_LINEAR',
        'NON_LIN': 'I_CAT_STATIC_NONLINEAR',
        'COMB_LINEAR': 'I_CAT_COMB',
        'COMB_NON_LIN': 'I_CAT_COMB_NONLINEAR'
    }
)
"""
Aliases for analysis type. For more details, see
``IRobotCaseAnalizeType``.

.. caution:: The typo is **in Robot API**, not this document.
"""


RLoadType = EnumCapsule(
    IRobotLoadRecordType,
    {
        'DEAD': 'I_LRT_DEAD',
        'NODAL': 'I_LRT_NODE_FORCE',
        'BAR_UDL': 'I_LRT_BAR_UNIFORM',
        'BAR_PL': 'I_LRT_BAR_FORCE_CONCENTRATED'
    }
)
"""
Aliases for load record types. For more details, see
``IRobotLoadRecordType``.
"""


RMatType = EnumCapsule(
    IRobotMaterialType,
    {
        'STEEL': 'I_MT_STEEL',
        'ALUM': 'I_MT_ALUMINIUM',
        'TIMBER': 'I_MT_TIMBER',
        'CONCRETE': 'I_MT_CONCRETE',
        'OTHER': 'I_MT_OTHER'
    }
)
"""
Aliases for material type. For more details, see
``IRobotMaterialType``.
"""


RReleaseValues = EnumCapsule(
    IRobotBarEndReleaseValue,
    {
        'NONE': 'I_BERV_NONE',
        'STD': 'I_BERV_STD',
        'FIXED': 'I_BERV_FIXED'
    }
)
"""
Aliases for bar end releases' values. For more details, see
``IRobotBarEndReleaseValue``.
"""


RDeadValues = EnumCapsule(
    IRobotDeadRecordValues,
    {
        'X': 'I_DRV_X',
        'Y': 'I_DRV_Y',
        'Z': 'I_DRV_Z',
        'COEFF': 'I_DRV_COEFF',
        'ENTIRE_STRUCT': 'I_DRV_ENTIRE_STRUCTURE'
    }
)
"""
Aliases for dead loads values. For more details, see
``IRobotDeadRecordValues``.
"""


RBarUDLValues = EnumCapsule(
    IRobotBarUniformRecordValues,
    {
        'FX': 'I_BURV_PX',
        'FY': 'I_BURV_PY',
        'FZ': 'I_BURV_PZ',
        'ALPHA': 'I_BURV_ALPHA',
        'BETA': 'I_BURV_BETA',
        'GAMMA': 'I_BURV_GAMMA',
        'IS_LOC': 'I_BURV_LOCAL',
        'IS_PROJ': 'I_BURV_PROJECTION',
        'IS_REL': 'I_BURV_RELATIVE',
        'OFFSET_Y': 'I_BURV_OFFSET_Y',
        'OFFSET_Z': 'I_BURV_OFFSET_Z'
    }
)
"""
Aliases for bars' uniform distributed loads. For more details, see
``IRobotBarUniformRecordValues``.
"""


RBarPLValues = EnumCapsule(
    IRobotBarForceConcentrateRecordValues,
    {
        'X': 'I_BFCRV_X',
        'FX': 'I_BFCRV_FX',
        'FY': 'I_BFCRV_FY',
        'FZ': 'I_BFCRV_FZ',
        'CX': 'I_BFCRV_CX',
        'CY': 'I_BFCRV_CY',
        'CZ': 'I_BFCRV_CZ',
        'ALPHA': 'I_BFCRV_ALPHA',
        'BETA': 'I_BFCRV_BETA',
        'GAMMA': 'I_BFCRV_GAMMA',
        'GEN_NODE': 'I_BFCRV_GENERATE_CALC_NODE',
        'IS_LOC': 'I_BFCRV_LOC',
        'IS_REL': 'I_BFCRV_REL',
        'OFFSET_Y': 'I_BFCRV_OFFSET_Y',
        'OFFSET_Z': 'I_BFCRV_OFFSET_Z'
    }
)
"""
Aliases for bars' point loads. For more details, see
``IRobotBarForceConcentrateRecordValues``.
"""


RLicense = EnumCapsule(
    IRobotLicenseEntitlement,
    {
        'LOCAL': 'I_LE_LOCAL_SOLVE',
        'CLOUD': 'I_LE_CLOUD_SOLVE'
    }
)
"""
Aliases for license entitlement. For more details see
``IRobotLicenseEntitlement``.
"""


RLicenseStatus = EnumCapsule(
    IRobotLicenseEntitlementStatus,
    {
        'OK': 'I_LES_ENTITLED'
    }
)
"""
Aliases for license status. For more details see
``IRobotLicenseEntitlementStatus``
"""
