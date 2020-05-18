import autorobot.extensions as extensions
from .errors import AutoRobotInitError

def requires_init(func):
    def wrapper(*args, **kwargs):
        if not extensions.app:
            raise(AutoRobotInitError, "Module `autoRobot` was not initialized.")
        app = extensions.app
        return func(*args, **kwargs)
    return wrapper