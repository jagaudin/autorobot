import clr
from pathlib import Path

from .errors import RobotPathError

p = Path(r'C:\Program Files\Autodesk')
suffix = r'System\EXE\interop.RobotOM.dll'

_robot_dll_path = str(next(p.rglob(suffix), ''))

try:
    clr.AddReference(_robot_dll_path)
except Exception as e:
    raise(RobotPathError(f"Couldn't find {p}\\*\\{suffix}"))

clr.AddReference(_robot_dll_path)

from RobotOM import (
    RobotApplicationClass,
)

ar = None