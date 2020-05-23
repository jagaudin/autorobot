class AutoRobotInitError(BaseException):
    '''An exception raised when the module was not initialized.'''
    pass


class AutoRobotProjError(BaseException):
    '''An exception raised when creating a new project failed.'''
    pass


class AutoRobotPathError(BaseException):
    '''An exception raised when the path to ``interop.RobotOM.dll`` is not valid.'''
    pass


class AutoRobotValueError(BaseException):
    '''An exception raised when an invalid value is encountered.'''
    pass


class AutoRobotIdError(BaseException):
    '''An exception raised when attempting to silently overwrite an object.'''
