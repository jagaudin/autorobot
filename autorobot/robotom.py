import clr
from pathlib import Path

from .errors import AutoRobotPathError

# Searching for ``interop.RobotOM.dll``
p = Path(r'C:\Program Files\Autodesk')

suffix = r'System\EXE\interop.RobotOM.dll'
_robot_dll_path = (
    str(p) if str(p).endswith(suffix)
    else str(next(p.rglob(suffix), ''))
)

try:
    clr.AddReference(_robot_dll_path)
except Exception as e:
    raise(AutoRobotPathError(f"Couldn't find {p}\\*\\{suffix}")) from e

clr.setPreload(True)
import RobotOM  # NOQA F401 F402
