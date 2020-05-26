from .constants import (
    RCaseNature,
    RCombType,
    RProjType,
    RAnalysisType
)

synonyms = {
    'BUILDING': RProjType.BUILDING,
    'FRAME_2D': RProjType.FRAME_2D,
    'FRAME_3D': RProjType.FRAME_3D,
    'SHELL': RProjType.SHELL,
    'TRUSS_2D': RProjType.TRUSS_2D,
    'TRUSS_3D': RProjType.TRUSS_3D,

    'PERM': RCaseNature.PERM,
    'IMPOSED': RCaseNature.IMPOSED,
    'WIND': RCaseNature.WIND,
    'SNOW': RCaseNature.SNOW,
    'ACC': RCaseNature.ACC,

    'SLS': RCombType.SLS,
    'ULS': RCombType.ULS,

    'LINEAR': RAnalysisType.LINEAR,
    'NON_LIN': RAnalysisType.NON_LIN,
    'COMB_LINEAR': RAnalysisType.COMB_LINEAR,
    'COMB_NON_LIN': RAnalysisType.COMB_NON_LIN,
}
"""A dictionary providing shorthands for commonly used constants.

The ``synonyms`` dictionary establishes correspondance between keyword
strings and some constants. Where supported, calling a method that
requires a constant as an argument can be done by providing a string
that gets translated into the constant through a look-up in
the ``synonyms`` dictionary.
"""

# Add the original constants to the dictionary
for e in (RCaseNature, RCombType, RProjType, RAnalysisType):
    synonyms.update({a: a.value for a in e})
