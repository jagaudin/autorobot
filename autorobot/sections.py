import autorobot.app as app

from .constants import (
    RLabelType,
    ROType,
)
from .decorators import requires_init
from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotNamesArray,
    IRobotBarSectionData,
    IRobotBarSectionNonstdDataValue,
    IRobotBarSectionShapeType,
    IRobotBarSectionType,
    IRobotLabel,
)


@requires_init
def create_section(name, h, w=0., t=0., shape='round', is_solid=True,
                   unit=1e-3):
    """Creates a custom section.

    The supported section shapes are round or rectangular, solid or hollow.

    :param str name: The section name
    :param float h, w, t:
       Height, width and thickness of the section (**w** and **t** may be
       omitted if not relevant).Dimensions are in mm by default (see **unit**).
    :param str shape: `'rect'` or `'round'`
    :param bool is_solid: Whether the section is solid
    :param float unit:
       The unit of section dimension relative to model unit (e.g. mm
       for a model in m: 1e-3)
    """
    h, w, t = unit * h, unit * w, unit * t

    shape_params = {
        ("round", True): {
            "type": IRobotBarSectionType.I_BST_NS_TUBE,
            "shapetype": IRobotBarSectionShapeType.I_BSST_USER_TUBE,
            "params": {
                IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_D: h,
                IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_T: 0.
            }
        },
        ("rect", True): {
            "type": IRobotBarSectionType.I_BST_NS_RECT,
            "shapetype": IRobotBarSectionShapeType.I_BSST_USER_RECT,
            "params": {
                IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_H: h,
                IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_B: w
            }
        },
        ("round", False): {
            "type": IRobotBarSectionType.I_BST_NS_TUBE,
            "shapetype": IRobotBarSectionShapeType.I_BSST_USER_TUBE,
            "params": {
                IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_D: h,
                IRobotBarSectionNonstdDataValue.I_BSNDV_TUBE_T: t
            }
        },
        ("rect", False): {
            "type": IRobotBarSectionType.I_BST_NS_RECT,
            "shapetype": IRobotBarSectionShapeType.I_BSST_USER_RECT,
            "params": {
                IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_H: h,
                IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_B: w,
                IRobotBarSectionNonstdDataValue.I_BSNDV_RECT_T: t
            }
        }
    }

    labels = app.app.structure.Labels
    section = IRobotLabel(labels.Create(RLabelType.BAR_SECT, name))
    data = IRobotBarSectionData(section.Data)
    data.Type = shape_params[(shape, is_solid)]['type']
    data.ShapeType = shape_params[(shape, is_solid)]['shapetype']

    nonstd_data = data.CreateNonstd(0.)  # Argument 0. is the position
    for arg, val in shape_params[(shape, is_solid)]["params"].items():
        nonstd_data.SetValue(arg, val)

    data.CalcNonstdGeometry()
    labels.StoreWithName(section, name)


@requires_init
def set_section(s, name):
    """Sets the section for a selection of bars.

    :param str s: A valid selection string
    :param str name: The section name
    """
    sel = app.selections.Create(ROType.BAR)
    sel.FromText(str(s))
    with app.bars as bars:
        bars.SetLabel(sel, RLabelType.BAR_SECT, name)


@requires_init
def list_section_db(filter=lambda s: True):
    """Returns the list of section database names.

    :param function filter: A condition to filter the result
    :return: List of section database names
    """
    db_list = app.Project.Preferences.SectionsFound
    db_list = [db_list.Get(i) for i in range(1, db_list.Count + 1)]
    return [name for name in db_list if filter(name)]


@requires_init
def get_section_db(name):
    """Returns the section database with the given name.

    :param str name: The database name
    :return:
       The section database with the given name as a ``IRobotSectionDatabase``
       instance.
    """
    db_list = app.Project.Preferences.SectionsFound
    return db_list.GetDatabase(db_list.Find(name))


@requires_init
def list_sections(db_name, filter=lambda s: True):
    """Returns the list of sections names in database.

    :param function filter: A condition to filter the result
    :return: List of section names
    """
    db = get_section_db(db_name)
    names = IRobotNamesArray(db.GetAll())
    names = [names.Get(i) for i in range(1, names.Count + 1)]
    return [name for name in names if filter(name)]


@requires_init
def load_section_from_db(name):
    """Loads a section from the database.

    :param str name: The name of the section
    """
    labels = app.structure.Labels
    section = IRobotLabel(labels.Create(RLabelType.BAR_SECT, name))
    data = IRobotBarSectionData(section.Data)
    data.LoadFromDBase(name)
    labels.Store(section)
