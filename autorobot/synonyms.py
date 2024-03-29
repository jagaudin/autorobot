from .constants import (
    RCaseNature,
    RCombType,
    RProjType,
    RAnalysisType
)

class ColanderDict(dict):
    """A dictionary that returns the key itself when it's missing."""

    def __missing__(self, key):
        """Method called when key is missing. Returns the key."""
        return key

synonyms = ColanderDict({
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
})
"""A dictionary providing shorthands for commonly used constants.

The ``synonyms`` dictionary establishes correspondance between keyword
strings and some constants. Where supported, calling a method that
requires a constant as an argument can be done by providing a string
that gets translated into the constant through a look-up in
the ``synonyms`` dictionary.
When the key is not present in the ``synonyms`` dictionary, the lookup
returns the key unchanged.
"""
