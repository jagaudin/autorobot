import numpy as np
import autorobot.app as app

from .constants import REditOpt
from .decorators import requires_init
from .synonyms import synonyms


class Axis:
    O = np.array((0., 0., 0.))
    X = np.array((1., 0., 0.))
    Y = np.array((0., 1., 0.))
    Z = np.array((0., 0., 1.))

@requires_init
def translate(otype, s, vector, copy=False, count=1):
    '''Translates a selection.

    :param int otype: The type of the object to be translated
    :param str s: A valid selection string
    :param tuple vector: The translation vector
    :param bool copy: Whether to copy the objects
    :paramint int count: Number of repetition of the transform

    .. tip:: This method supports :ref:`about_synonyms` for the
      **otype** argument. For example: ::

            translate('NODE', '1', (1., 0., 0.))
    '''
    app.app.selections.clear_current()
    sel = app.app.selections.Get(synonyms[otype])
    sel.FromText(s)
    copy = REditOpt.COPY if copy else REditOpt.MOVE
    app.app.structure.Edit.SelTranslate(*vector, copy, count)
    sel.Clear()


@requires_init
def rotate(otype, s, axis_start, axis_end, angle, copy=False, count=1,
           rad=False):
    '''Rotates a selection.

    :param int otype: The type of the object to be rotated
    :param str s: A valid selection string
    :param tuple axis_start, axis_end: Two points defining the rotation axis
    :param float angle: The angle (in degrees by default)
    :param bool copy: Whether to copy the objects
    :param bool rad: Whether the angle is given in radians
    :paramint int count: Number of repetition of the transform

    .. tip:: This method supports :ref:`about_synonyms` for the
      **otype** argument. For example: ::

            rotate('NODE', '1', (0., 0., 0.), (0., 0., 1.), 30.)
    '''
    app.app.selections.clear_current()
    sel = app.app.selections.Get(synonyms[otype])
    sel.FromText(s)
    copy = REditOpt.COPY if copy else REditOpt.MOVE
    angle = angle if rad else np.radians(angle)
    app.app.structure.Edit.SelRotate(
        *axis_start, *axis_end, angle, copy, count)
    sel.Clear()
