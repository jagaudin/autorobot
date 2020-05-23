from .constants import (
    RBarPLValues,
    RBarUDLValues,
    RLoadType,
)
from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotLoadRecord,
)


def add_bar_udl(case, s, desc='', fx=0., fy=0., fz=0., alpha=0., beta=0., gamma=0.,
                is_local=False, is_proj=False, is_relative=False, offset_y=0., offset_z=0.):
    '''Adds a uniformly distributed load on a selection of bars.

    :param IRobotCase case: The load case to be modified
    :param str s: A valid bar selection string
    :param str desc: A description (optional)
    :param float fx, fy, fz: Force vector
    :param float alpha, beta, gamma: Rotation of the force vector
    :param bool is_local: Whether the force is defined in local coordinates
    :param bool is_proj: Whether the force is projected
    :param boll is_relative: Whether the position `x` is relative
    :param float offset_y, offset_z: Force vector offset from the bar
    '''
    rec_num = case.Records.New(RLoadType.BAR_UDL)
    rec = IRobotLoadRecord(case.Records.Get(rec_num))

    rec.Objects.FromText(s)
    rec.Description = desc

    rec_values = {
        RBarUDLValues.FX: fx * 1e3,
        RBarUDLValues.FY: fy * 1e3,
        RBarUDLValues.FZ: fz * 1e3,
        RBarUDLValues.ALPHA: alpha,
        RBarUDLValues.BETA: beta,
        RBarUDLValues.GAMMA: gamma,
        RBarUDLValues.IS_LOC: is_local,
        RBarUDLValues.IS_PROJ: is_proj,
        RBarUDLValues.IS_REL: is_relative,
        RBarUDLValues.OFFSET_Y: offset_y,
        RBarUDLValues.OFFSET_Z: offset_z,
    }

    for k, v in rec_values.items():
        rec.SetValue(k, v)


def add_bar_pl(case, s, desc='', x=0., fx=0., fy=0., fz=0., alpha=0., beta=0., gamma=0.,
               is_local=False, is_relative=False, offset_y=0., offset_z=0.):
    '''Adds a point load on a selection of bars.

    :param IRobotCase case: The load case to be modified
    :param str s: A valid bar selection string
    :param str desc: A description (optional)
    :param float x: The location of the load on the bar
    :param float fx, fy, fz: Force vector
    :param float alpha, beta, gamma: Rotation of the force vector
    :param bool is_local: Whether the force is defined in local coordinates
    :param bool is_relative: Whether the position ``x`` is relative
    :param float offset_y, offset_z: Force vector offset from the bar
    '''
    rec_num = case.Records.New(RLoadType.BAR_PL)
    rec = IRobotLoadRecord(case.Records.Get(rec_num))

    rec.Objects.FromText(s)
    rec.Description = desc

    rec_values = {
        RBarPLValues.X: x,
        RBarPLValues.FX: fx * 1e3,
        RBarPLValues.FY: fy * 1e3,
        RBarPLValues.FZ: fz * 1e3,
        RBarPLValues.ALPHA: alpha,
        RBarPLValues.BETA: beta,
        RBarPLValues.GAMMA: gamma,
        RBarPLValues.IS_LOC: is_local,
        RBarPLValues.IS_REL: is_relative,
        RBarPLValues.OFFSET_Y: offset_y,
        RBarPLValues.OFFSET_Z: offset_z,
    }

    for k, v in rec_values.items():
        rec.SetValue(k, v)
