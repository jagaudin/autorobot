import numpy as np

from .constants import (
    RBarPLValues,
    RBarUDLValues,
    RCaseNature,
    RCaseType,
    RDeadValues,
    RLoadType,
    ROType,
)
from .extensions import (
    Capsule,
    ExtendedServer,
)
from .synonyms import synonyms

from .errors import (
    AutoRobotIdError,
)

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotCase,
    IRobotCaseCombination,
    IRobotCaseServer,
    IRobotLoadRecord,
    IRobotSimpleCase,
)


class ExtendedSimpleCase(Capsule):
    """
    This class is an extension for ``IRbotCase`` providing the methods
    and properties listed below in addition to the methods of the
    original object.
    """

    _otype = IRobotSimpleCase

    load_type_values = {
        RLoadType.DEAD: RDeadValues,
        RLoadType.BAR_UDL: RBarUDLValues,
        RLoadType.BAR_PL: RBarPLValues,
    }

    @property
    def loads(self):
        """The list of loads defined."""
        n = self.Records.Count
        _loads = []
        for i in range(1, n + 1):
            rec = self.get(i)
            load = {'Type': rec.Type, 'Description': rec.Description}
            if self.load_type_values.get(rec.Type, None):
                index = self.load_type_values[rec.Type].custom_index
                for k, v in index.items():
                    load[k] = self.get_record_value(rec, v)
            _loads.append(load)
        return _loads

    def add_self_weight(self, s='all', factor=1., desc=''):
        """Adds self-weight forces to the structure.

        :param str s: A valid bar selection string (default: `'all'`')
        :param factor: A factor applied on the self-weight

        .. note:
           The self-weight forces are applied in the negative Z
           direction.
        """
        rec = IRobotLoadRecord(self.Records.Create(RLoadType.DEAD))
        rec.Objects.FromText(str(s))
        rec.Description = desc
        self.set_record_value(rec, RDeadValues.Z, -1.)
        self.set_record_value(rec, RDeadValues.COEFF, factor)
        if s.lower() == 'all':
            self.set_record_value(rec, RDeadValues.ENTIRE_STRUCT, True)

    def add_bar_udl(self, s, fx=0., fy=0., fz=0.,
                    alpha=0., beta=0., gamma=0.,
                    is_local=False, is_proj=False, is_relative=False,
                    offset_y=0., offset_z=0.,
                    unit=1e3, unit_angle=np.pi / 180, desc=''):
        """Adds a uniformly distributed load on a selection of bars.

        :param str s: A valid bar selection string
        :param str desc: A description (optional)
        :param float fx, fy, fz: Force vector
        :param float alpha, beta, gamma: Rotation of the force vector
        :param bool is_local: Whether the force is defined in local coordinates
        :param bool is_proj: Whether the force is projected
        :param boll is_relative: Whether the position `x` is relative
        :param float offset_y, offset_z: Force vector offset from the bar
        :param float unit: A multiplication factor for the force input
        :param float unit_angle: A multiplication factor for angle input
        """
        rec = IRobotLoadRecord(self.Records.Create(RLoadType.BAR_UDL))
        rec.Objects.FromText(str(s))
        rec.Description = desc
        rec_values = {
            RBarUDLValues.FX: fx * unit,
            RBarUDLValues.FY: fy * unit,
            RBarUDLValues.FZ: fz * unit,
            RBarUDLValues.ALPHA: alpha * unit_angle,
            RBarUDLValues.BETA: beta * unit_angle,
            RBarUDLValues.GAMMA: gamma * unit_angle,
            RBarUDLValues.IS_LOC: is_local,
            RBarUDLValues.IS_PROJ: is_proj,
            RBarUDLValues.IS_REL: is_relative,
            RBarUDLValues.OFFSET_Y: offset_y,
            RBarUDLValues.OFFSET_Z: offset_z,
        }
        for k, v in rec_values.items():
            self.set_record_value(rec, k, v)

    def add_bar_pl(self, s, x=0., fx=0., fy=0., fz=0., alpha=0.,
                   beta=0., gamma=0., is_local=False, is_relative=False,
                   offset_y=0., offset_z=0.,
                   unit=1e3, unit_angle=np.pi / 180, desc=''):
        """Adds a point load on a selection of bars.

        :param str s: A valid bar selection string
        :param str desc: A description (optional)
        :param float x: The location of the load on the bar
        :param float fx, fy, fz: Force vector
        :param float alpha, beta, gamma: Rotation of the force vector
        :param bool is_local: Whether the force is defined in local coordinates
        :param bool is_relative: Whether the position ``x`` is relative
        :param float offset_y, offset_z: Force vector offset from the bar
        :param float unit: A multiplication factor for the force input
        :param float unit_angle: A multiplication factor for angle input
        """
        rec = IRobotLoadRecord(self.Records.Create(RLoadType.BAR_PL))
        rec.Objects.FromText(str(s))
        rec.Description = desc
        rec_values = {
            RBarPLValues.X: x,
            RBarPLValues.FX: fx * unit,
            RBarPLValues.FY: fy * unit,
            RBarPLValues.FZ: fz * unit,
            RBarPLValues.ALPHA: alpha * unit_angle,
            RBarPLValues.BETA: beta * unit_angle,
            RBarPLValues.GAMMA: gamma * unit_angle,
            RBarPLValues.IS_LOC: is_local,
            RBarPLValues.IS_REL: is_relative,
            RBarPLValues.OFFSET_Y: offset_y,
            RBarPLValues.OFFSET_Z: offset_z,
        }
        for k, v in rec_values.items():
            self.set_record_value(rec, k, v)

    def delete(self, n):
        """Deletes the load record at index n.

        :param int n: The load record number
        """
        self.Records.Delete(n)

    def get(self, n):
        """Returns the load record at index n.

        :param int n: The load record number
        """
        return IRobotLoadRecord(self.Records.Get(n))

    @staticmethod
    def get_record_value(record, key):
        """
        Gets a value from a load record.

        :param obj record: A load record
        :param obj key: The key for the value to get (an Enum member)
        :return: The value contained in the record

        Because the record types are varied, the ``GetValue`` method for the
        records takes an integer argument and not an Enum-like type. Since v3,
        PythonNet doesn't convert Enum to int automatically, hence this helper
        method to cast the Enum to int.
        """
        return record.GetValue(int(key))

    @staticmethod
    def set_record_value(record, key, value):
        """
        Sets a value on a load record.

        :param obj record: A load record
        :param obj key: The key for the value to be set (an Enum member)
        :param float value: The value to be set

        Because the record types are varied, the ``SetValue`` method for the
        records takes an integer argument and not an Enum-like type. Since v3,
        PythonNet doesn't convert Enum to int automatically, hence this helper
        method to cast the Enum to int.
        """
        record.SetValue(int(key), value)


class ExtendedCaseServer(ExtendedServer):
    """
    This class is an extension for ``IRobotCaseServer`` providing
    additional functions for the management of load cases.
    """

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
            return ExtendedSimpleCase(IRobotSimpleCase(case))
        elif case.Type == RCaseType.COMB:
            return IRobotCaseCombination(case)

    def create_case(self, num, name, nature, analysis_type,
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

                create_case(1, 'Load case', 'IMPOSED', 'LINEAR')
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
        return ExtendedSimpleCase(IRobotSimpleCase(case))

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
        return self.cast(super(ExtendedCaseServer, self).get(int(n)))

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
