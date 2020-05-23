from .extensions import initialize

from .constants import (
    _robot_dll_path,
    RProjType,
    ROType,
)

from .loads import (
    add_bar_udl,
    add_bar_pl,
)

from .nodes import (
    distance,
)

import clr
clr.AddReference(_robot_dll_path)
import RobotOM
