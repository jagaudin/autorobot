import numpy as np

from functools import wraps

import autorobot.app as app

from .constants import (
    RBarPLValues,
    RBarUDLValues,
    RDeadValues,
)

from .extensions import Capsule

from .robotom import RobotOM  # NOQA F401
from RobotOM import (
    IRobotLoadRecord,
)


def _getter_setter_factory(key, as_bool=False, unit=0.):
    '''Creates property getter and setter for a given key.

       Additional arguments can be used to cast of scale the original property.
    '''
    def getter(self):
        '''Generic getter.'''
        return self.GetValue(int(key))

    def setter(self, value):
        '''Generic setter.'''
        self.SetValue(int(key), float(value))

    def booleify(getter):
        '''Casts the result of a getter to boolean.'''
        @wraps(getter)
        def wrapper(*args, **kwargs):
            return bool(getter(*args, **kwargs))

        return wrapper

    def convert_to(unit):
        '''Returns a getter decorator that encapsulate a unit function.'''
        def decorator(getter):
            @wraps(getter)
            def wrapper(*args, **kwargs):
                return getter(*args, **kwargs) / unit()
            return wrapper
        return decorator

    def convert_from(unit):
        '''Returns a setter decorator that encapsulate a unit function.'''
        def decorator(setter):
            @wraps(setter)
            def wrapper(self, value, *args, **kwargs):
                setter(self, value * unit(), *args, **kwargs)
            return wrapper
        return decorator

    if as_bool:
        return booleify(getter), setter
    elif unit:
        return convert_to(unit)(getter), convert_from(unit)(setter)
    else:
        return getter, setter


class ExtendedLoadRecord(Capsule):

    _otype = IRobotLoadRecord


class ExtendedSelfWeightRecord(ExtendedLoadRecord):

    x = property(
        *_getter_setter_factory(RDeadValues.X),
        doc='Self-weight coefficient.'
    )

    y = property(
        *_getter_setter_factory(RDeadValues.Y),
        doc='Self-weight coefficient.'
    )

    z = property(
        *_getter_setter_factory(RDeadValues.Z),
        doc='Self-weight coefficient.'
    )

    coeff = property(
        *_getter_setter_factory(RDeadValues.COEFF),
        doc='Self-weight coefficient.'
    )

    entire_struct = property(
        *_getter_setter_factory(RDeadValues.ENTIRE_STRUCT, as_bool=True),
        doc='Whether the self-weight is applied to the entire structure.'
    )


class ExtendedBarUDLRecord(ExtendedLoadRecord):

    fx = property(
        *_getter_setter_factory(
            RBarUDLValues.I_BURV_PX, unit=lambda: app.get_app().unit_force),
        doc='Force in the X axis.'
    )
    fy = property(
        *_getter_setter_factory(
            RBarUDLValues.I_BURV_PY, unit=lambda: app.get_app().unit_force),
        doc='Force in the Y axis.'
    )
    fz = property(
        *_getter_setter_factory(
            RBarUDLValues.I_BURV_PZ, unit=lambda: app.get_app().unit_force),
        doc='Force in the Z axis.'
    )
    alpha = property(
        *_getter_setter_factory(
            RBarUDLValues.I_BURV_ALPHA,
            unit=lambda: app.get_app().unit_angle_in
        ),
        doc='Rotation angle of the force vector.'
    )
    beta = property(
        *_getter_setter_factory(
            RBarUDLValues.I_BURV_BETA,
            unit=lambda: app.get_app().unit_angle_in
        ),
        doc='Rotation angle of the force vector.'
    )
    gamma = property(
        *_getter_setter_factory(
            RBarUDLValues.I_BURV_GAMMA,
            unit=lambda: app.get_app().unit_angle_in
        ),
        doc='Rotation angle of the force vector.'
    )
    is_local = property(
        *_getter_setter_factory(RBarUDLValues.I_BURV_LOCAL, as_bool=True),
        doc='Whether the force is defined in local coordinates.'
    )
    is_projected = property(
        *_getter_setter_factory(RBarUDLValues.I_BURV_PROJECTION, as_bool=True),
        doc='Whether the force is projected in plan.'
    )
    is_relative = property(
        *_getter_setter_factory(RBarUDLValues.I_BURV_RELATIVE, as_bool=True),
        doc='Whether the force is projected in plan.'
    )
    offset_y = property(
        *_getter_setter_factory(RBarUDLValues.I_BURV_OFFSET_Y),
        doc='Offset of load in the local Y direction.'
    )
    offset_z = property(
        *_getter_setter_factory(RBarUDLValues.I_BURV_OFFSET_Z),
        doc='Offset of load in the local Z direction.'
    )


class ExtendedBarPLRecord(ExtendedLoadRecord):

    @property
    def x(self):
        """Position along bar."""
        unit = app.get_app().unit_length if not self.is_relative else 1.
        return self.GetValue(int(RBarPLValues.I_BFCRV_X)) / unit

    @x.setter
    def x(self, value):
        unit = app.get_app().unit_length if not self.is_relative else 1.
        self.SetValue(int(RBarPLValues.I_BFCRV_X), value * unit)

    fx = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_FX, unit=lambda: app.get_app().unit_force),
        doc='Force in the X axis.'
    )
    fy = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_FY, unit=lambda: app.get_app().unit_force),
        doc='Force in the Y axis.'
    )
    fz = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_FZ, unit=lambda: app.get_app().unit_force),
        doc='Force in the Z axis.'
    )
    cx = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_CX,
            unit=lambda: app.get_app().unit_force * app.get_app().unit_length),
        doc='Moment in the X axis.'
    )
    cy = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_CY,
            unit=lambda: app.get_app().unit_force * app.get_app().unit_length),
        doc='Moment in the Y axis.'
    )
    cz = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_CZ,
            unit=lambda: app.get_app().unit_force * app.get_app().unit_length),
        doc='Moment in the Z axis.'
    )
    alpha = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_ALPHA,
            unit=lambda: app.get_app().unit_angle_in
        ),
        doc='Rotation angle of the force vector.'
    )
    beta = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_BETA,
            unit=lambda: app.get_app().unit_angle_in
        ),
        doc='Rotation angle of the force vector.'
    )
    gamma = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_GAMMA,
            unit=lambda: app.get_app().unit_angle_in
        ),
        doc='Rotation angle of the force vector.'
    )
    gen_node = property(
        *_getter_setter_factory(
            RBarPLValues.I_BFCRV_GENERATE_CALC_NODE, as_bool=True),
        doc='Whether a node is generated a position.'
    )
    is_local = property(
        *_getter_setter_factory(RBarPLValues.I_BFCRV_LOC, as_bool=True),
        doc='Whether the force is defined in local coordinates.'
    )
    is_relative = property(
        *_getter_setter_factory(RBarPLValues.I_BFCRV_REL, as_bool=True),
        doc='Whether the force is projected in plan.'
    )
    offset_y = property(
        *_getter_setter_factory(RBarPLValues.I_BFCRV_OFFSET_Y),
        doc='Offset of load in the local Y direction.'
    )
    offset_z = property(
        *_getter_setter_factory(RBarPLValues.I_BFCRV_OFFSET_Z),
        doc='Offset of load in the local Z direction.'
    )
