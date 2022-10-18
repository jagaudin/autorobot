import clr
from System.Runtime.InteropServices import COMException

class AutoRobotInitError(BaseException):
    """Raised when the module was not initialized."""


class AutoRobotProjError(BaseException):
    """Raised when creating a new project failed."""


class AutoRobotPathError(BaseException):
    """Raised when the path to ``interop.RobotOM.dll`` is not valid."""


class AutoRobotValueError(BaseException):
    """Raised when an invalid value is encountered."""


class AutoRobotIdError(BaseException):
    """Raised when attempting to silently overwrite an object."""


class AutoRobotLicenseError(BaseException):
    """Raised when the license is not available."""
    msg = "License error, check if it is available."
