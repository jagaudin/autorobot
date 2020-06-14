import autorobot.app as app

from .constants import (
    RLabelType,
    ROType,
)
from .decorators import requires_init

from .extensions import (
    ExtendedLabel,
    ExtendedLabelServer,
)

from .errors import (
    AutoRobotValueError,
)

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotNamesArray,
    IRobotBarSectionData,
    IRobotBarSectionDataValue,
    IRobotBarSectionNonstdData,
    IRobotBarSectionNonstdDataValue,
    IRobotBarSectionShapeType,
    IRobotBarSectionType,
    IRobotLabel,
    IRobotLabelServer,
)


class ExtendedSectionLabel(ExtendedLabel):
    """
    This class is an extension for ``IRobotLabel`` providing new
    methods in addition to the methods of the original object.
    """

    _otype = IRobotLabel
    _dtype = IRobotBarSectionData

    @property
    def IX(self):
        """Torsion constant of the section."""
        return self.data.GetValue(IRobotBarSectionDataValue.I_BSDV_IX)

    @property
    def IY(self):
        """Second moment of area in the Y axis."""
        return self.data.GetValue(IRobotBarSectionDataValue.I_BSDV_IY)

    @property
    def IZ(self):
        """Second moment of area in the Z axis."""
        return self.data.GetValue(IRobotBarSectionDataValue.I_BSDV_IZ)

    @property
    def d(self):
        """Depth or diameter of the section."""
        if self.data.NonstdCount > 1:
            raise AutoRobotValueError("Can't get depth of tapered section.")
        elif self.data.NonstdCount == 1:
            ns_data = IRobotBarSectionNonstdData(self.data.GetNonstd(1))
            if self.data.Type == IRobotBarSectionType.I_BST_NS_TUBE:
                return ns_data.GetValue(
                    IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_D)
            elif self.data.Type == IRobotBarSectionType.I_BST_NS_RECT:
                return ns_data.GetValue(
                    IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_H)
        else:
            return self.data.GetValue(IRobotBarSectionDataValue.I_BSDV_D)

    @property
    def b(self):
        """Width of the section."""
        if self.data.NonstdCount > 1:
            raise AutoRobotValueError("Can't get width of tapered section.")
        elif self.data.NonstdCount == 1:
            ns_data = IRobotBarSectionNonstdData(self.data.GetNonstd(1))
            if self.data.Type == IRobotBarSectionType.I_BST_NS_TUBE:
                return ns_data.GetValue(
                    IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_D)
            elif self.data.Type == IRobotBarSectionType.I_BST_NS_RECT:
                return ns_data.GetValue(
                    IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_B)
        else:
            return self.data.GetValue(IRobotBarSectionDataValue.I_BSDV_BF)

    @property
    def t(self):
        """Thickness of the section."""
        if self.data.NonstdCount > 1:
            raise AutoRobotValueError(
                "Can't get thickness of tapered section.")
        elif self.data.NonstdCount == 1:
            ns_data = IRobotBarSectionNonstdData(self.data.GetNonstd(1))
            if self.data.Type == IRobotBarSectionType.I_BST_NS_TUBE:
                return ns_data.GetValue(
                    IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_T)
            elif self.data.Type == IRobotBarSectionType.I_BST_NS_RECT:
                return ns_data.GetValue(
                    IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_T)
        else:
            return self.data.GetValue(IRobotBarSectionDataValue.I_BSDV_TF)

    @property
    def weight(self):
        """"Linear weight of the section."""
        return self.data.GetValue(IRobotBarSectionDataValue.I_BSDV_WEIGHT)


class ExtendedSectionServer(ExtendedLabelServer):
    """
    This class is an extension for ``IRobotLabelServer`` providing
    additional functions for the management of section labels.
    """

    _otype = IRobotLabelServer
    _ctype = IRobotLabel
    _ltype = RLabelType.BAR_SECT
    _dtype = IRobotBarSectionData
    _rtype = ExtendedSectionLabel

    def create(self, name, h, w=0., t=0., shape='round', is_solid=True,
               material='', unit=1e-3):
        """Creates a custom section.

        The supported section shapes are round or rectangular, solid or
        hollow.

        :param str name: The section name
        :param float h, w, t:
           Height, width and thickness of the section (**w** and **t** may be
           omitted if not relevant).Dimensions are in mm by default
           (see **unit**).
        :param str shape: `'rect'` or `'round'`
        :param bool is_solid: Whether the section is solid
        :param float unit:
           The unit of section dimension relative to model unit (e.g. mm
           for a model in m: 1e-3)
        """
        h, w, t, shape = unit * h, unit * w, unit * t, str(shape).lower()

        shape_params = {
            ('round', True): {
                'type': IRobotBarSectionType.I_BST_NS_TUBE,
                'shapetype': IRobotBarSectionShapeType.I_BSST_USER_TUBE,
                'params': {
                    IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_D: h,
                    IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_T: 0.
                }
            },
            ('rect', True): {
                'type': IRobotBarSectionType.I_BST_NS_RECT,
                'shapetype': IRobotBarSectionShapeType.I_BSST_USER_RECT,
                'params': {
                    IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_H: h,
                    IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_B: w
                }
            },
            ('round', False): {
                'type': IRobotBarSectionType.I_BST_NS_TUBE,
                'shapetype': IRobotBarSectionShapeType.I_BSST_USER_TUBE,
                'params': {
                    IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_D: h,
                    IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_T: t
                }
            },
            ('rect', False): {
                'type': IRobotBarSectionType.I_BST_NS_RECT,
                'shapetype': IRobotBarSectionShapeType.I_BSST_USER_RECT,
                'params': {
                    IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_H: h,
                    IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_B: w,
                    IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_T: t
                }
            }
        }

        label = self._ctype(self.Create(self._ltype, name))
        data = self._dtype(label.Data)
        data.Type = shape_params[(shape, is_solid)]['type']
        data.ShapeType = shape_params[(shape, is_solid)]['shapetype']
        if material:
            data.MaterialName = material

        nonstd_data = data.CreateNonstd(0.)  # Argument 0. is the position
        for arg, val in shape_params[(shape, is_solid)]['params'].items():
            nonstd_data.SetValue(arg, val)

        data.CalcNonstdGeometry()
        self.StoreWithName(label, name)

    def set(self, s, name):
        """Sets the section for a selection of bars.

        :param str s: A valid selection string
        :param str name: The section name
        """
        sel = self.app.selections.Create(ROType.BAR)
        sel.FromText(str(s))
        with self.app.bars as bars:
            bars.SetLabel(sel, RLabelType.BAR_SECT, name)

    def db_list(self, func=lambda s: True):
        """Returns the list of section database names.

        :param function func: A condition to filter the result
        :return: List of section database names
        """
        db_list = self.app.Project.Preferences.SectionsFound
        db_list = [db_list.Get(i) for i in range(1, db_list.Count + 1)]
        return [name for name in db_list if func(name)]

    def get_db(self, name):
        """Returns the section database with the given name.

        :param str name: The database name
        :return:
           The section database with the given name as a
           ``IRobotSectionDatabase`` instance.
        """
        db_list = self.app.Project.Preferences.SectionsFound
        return db_list.GetDatabase(db_list.Find(str(name)))

    def get_db_names(self, db_name, func=lambda s: True):
        """Returns the list of sections names in database.

        :param str db_name: The name of the database to use for lookup
        :param function func: A condition to filter the result
        :return: List of section names
        """
        db = self.get_db(db_name)
        names = IRobotNamesArray(db.GetAll())
        names = [names.Get(i) for i in range(1, names.Count + 1)]
        return [name for name in names if func(name)]

    def load(self, name, db_name=''):
        """Loads a section from a database.

        :param str name: The name of the section
        :param str db_name: The name of the database to use for lookup
        """
        label = self._ctype(self.Create(self._ltype, name))
        data = self._dtype(label.Data)
        if db_name:
            success = data.LoadFromDBase2(name, db_name)
        else:
            success = data.LoadFromDBase(name)
        if success:
            self.Store(label)
