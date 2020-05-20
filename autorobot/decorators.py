from abc import ABC
from functools import wraps
import autorobot.extensions as extensions
from .errors import AutoRobotInitError

def requires_init(func):
    '''Function decorator to provide the autorobot context to a function.'''
    
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not extensions.app:
            raise(AutoRobotInitError, "Module `autoRobot` was not initialized.")
        app = extensions.app
        return func(*args, **kwargs)
    return wrapper


def abstract_attributes(*names):
    '''Class decorator to add abstract attributes.'''
    
    def factory(cls):
        '''A function returning the result of ``extend_init_subclass``.'''
        
        def extend_init_subclass(cls, *names):
            '''Function that extends the __init_subclass__ method of a class.'''

            # Assign NotImplemented to each abstract attribute
            for name in names:
                setattr(cls, name, NotImplemented)

            # Save the original __init_subclass__ implementation
            orig_init_subclass = cls.__init_subclass__

            def new_init_subclass(cls, **kwargs):
                '''New definition of __init_subclass__'''

                # The default implementation of __init_subclass__ takes no
                # positional arguments, but a custom implementation does.
                # If the user has not reimplemented __init_subclass__ then
                # the first signature will fail and we try the second.
                try:
                    orig_init_subclass(cls, **kwargs)
                except TypeError:
                    orig_init_subclass(**kwargs)

                # Check if ABC is in the class bases and check attributes if not
                if ABC not in cls.__bases__:
                    for name in names:
                        if getattr(cls, name, NotImplemented) is NotImplemented:
                            raise NotImplementedError(
                                f"`{name}` must be a class attribute of `{cls.__name__}`."
                            )

            # Bind this new function to the __init_subclass__
            cls.__init_subclass__ = classmethod(new_init_subclass)

            return cls
        
        return extend_init_subclass(cls, *names)
        
    return factory