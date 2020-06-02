from .constants import (
    RCaseNature,
    RCaseType,
    ROType,
)
from .extensions import ExtendedServer
from .synonyms import synonyms

from .errors import (
    AutoRobotIdError,
)

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotCase,
    IRobotCaseCombination,
    IRobotCaseServer,
    IRobotSimpleCase,
)


class ExtendedCaseServer(ExtendedServer):

    _otype = IRobotCaseServer
    _ctype = IRobotCase
    _dtype = ROType.CASE
    _rtype = IRobotCase

    label_prefix = {
        RCaseNature.PERM: 'G',
        RCaseNature.IMPOSED: 'Q',
        RCaseNature.WIND: 'W',
        RCaseNature.SNOW: 'S',
        RCaseNature.ACC: 'A',
    }
    """
    A dictionary providing prefixes for labelling to load cases based on
    their nature. The label is formed of the prefix and the case number. The
    values can be changed to suit preferences. The default prefixes are:

     * ``RCaseNature.PERM``: ``'G'``,
     * ``RCaseNature.IMPOSED``: ``'Q'``,
     * ``RCaseNature.WIND``: ``'W'``,
     * ``RCaseNature.SNOW``: ``'S'``,
     * ``RCaseNature.ACC``: ``'A'``,

    .. caution:: There is a distinction between a load case *label* and its
       *name*. The label of a load cases is usually shorter than its name.
    """

    @staticmethod
    def cast(case):
        """Casts a load case object according to its type.

        :param IRobotCase case: The load case object
        """
        if case.Type == RCaseType.SIMPLE:
            return IRobotSimpleCase(case)
        elif case.Type == RCaseType.COMB:
            return IRobotCaseCombination(case)

    def create_load_case(self, num, name, nature, analysis_type,
                         overwrite=False):
        """Creates a new load case.

        :param int num: The load case number
        :param str name: Name of the load case
        :param int nature: Nature of the load case (see `RCaseNature`)
        :param int analysis_type: Type of analysis (see `RAnalysisType`)
        :param bool overwrite:
           Whether to override if number conflicts with existing data
        :return: The load case object (as a ``IRobotSimpleCase`` instance)

        .. tip:: This method supports :ref:`about_synonyms` for the
          **nature** and **analysis_type** arguments. For example: ::

                create_load_case(1, 'Load case', 'IMPOSED', 'LINEAR')
        """
        if num is None:
            num = self.FreeNumber
        num = int(num)
        if self.Exist(num):
            if overwrite:
                self.Delete(num)
            else:
                raise AutoRobotIdError(f"Case with id {num} already exists.")
        case = IRobotSimpleCase(
            self.CreateSimple(num, name, synonyms[nature],
                              synonyms[analysis_type]))
        case.label = self.label_prefix[synonyms[nature]] + str(num)
        return case

    def create_combination(self, num, name, case_factors, comb_type, nature,
                           analysis_type, overwrite=False):
        """Creates a new load case combination.

        :param int num: The load case number
        :param str name: Name of the combination
        :param dict case_factors: A dict of (case, factor) pairs
        :param int comb_type: The type of the combination (see `RCombType`)
        :param int nature: Nature of the load case (see `RCaseNature`)
        :param int analysis_type: Type of analysis (see `RAnalysisType`)
        :param bool overwrite: Whether to overwrite if case id already exists
        :return:
           The load combination object (as an ``IRobotCaseCombination``
           instance)

        .. tip:: This method supports :ref:`about_synonyms` for the
          **comb_type**, **nature** and **analysis_type** arguments.
          For example: ::

                create_combination(1, 'Comb', 'SLS', 'PERM', 'COMB_LINEAR')
        """
        if num is None:
            num = self.FreeNumber
        num = int(num)
        if self.Exist(num):
            if overwrite:
                self.Delete(num)
            else:
                raise AutoRobotIdError(f"Case with id {num} already exists.")
        comb = IRobotCaseCombination(
            self.CreateCombination(num, name, synonyms[comb_type],
                                   synonyms[nature], synonyms[analysis_type]))
        for k, v in case_factors.items():
            comb.CaseFactors.New(k, v)
        return comb

    def get(self, n):
        """A method to retrieve load case objects from the server.

        :param int n: The case number

        .. note::

           The function casts the argument **n** to ``int`` before querying
           the server.
        """
        return self.cast(super(ExtendedCaseServer, self).get(n))

    def select(self, s, obj=True):
        """
        Returns an iterator of load case objects referred to in a selection
        string.

        :param str s: A valid selection string
        :param bool obj: Whether to return case objects or cases' numbers
        :return: A generator of the selected load cases
        """
        it = super(ExtendedCaseServer, self).select(s, obj)
        if not obj:
            return it
        else:
            for c in it:
                yield self.cast(c)
