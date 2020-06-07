from .extensions import (
    ExtendedLabel,
    ExtendedLabelServer,
)

from .constants import RLabelType

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotLabel,
    IRobotLabelServer,
    IRobotMaterialData,
    IRobotNamesArray,
)


class ExtendedMaterialLabel(ExtendedLabel):
    """
    This class is an extension for ``IRobotLabel`` providing the
    mehtods listed below in addition to the methods of the original object.
    """

    _otype = IRobotLabel
    _dtype = IRobotMaterialData

    @property
    def is_default(self):
        """Indicates whether the material is the default material."""
        return self.data.Default

    @property
    def density(self):
        """Density of the material."""
        return self.data.RO

    @property
    def RO(self):
        """Density of the material."""
        return self.data.RO

    @property
    def E(self):
        """Young's modulus of the material."""
        return self.data.E

    @property
    def G(self):
        """Shear modulus of the material."""
        return self.data.Kirchoff

    @property
    def NU(self):
        """Poisson's ratio of the material."""
        return self.data.NU

    @property
    def fy(self):
        """Yield strength of the material."""
        return self.data.RE

    @property
    def RE(self):
        """Compressive strength of the material."""
        return self.data.RE


class ExtendedMaterialServer(ExtendedLabelServer):
    """
    This class is an extension for ``IRobotLabelServer`` providing
    additional functions for the management of material labels. 
    """

    _otype = IRobotLabelServer
    _ctype = IRobotLabel
    _ltype = RLabelType.MAT
    _dtype = IRobotMaterialData
    _rtype = ExtendedMaterialLabel

    def get_names_db(self, func=lambda s: True):
        '''Returns the list of material names in database.

        :param function func: A filter function
        :return: The list of material names in the database
        '''
        db = self.app.Project.Preferences.Materials
        names = IRobotNamesArray(db.GetAll())
        names = [names.Get(i) for i in range(1, names.Count + 1)]
        return [name for name in names if cond(name)]
