from .exceptions import *

VERSION = '1.0.1'

ENGINE_CLASSES = []
REGISTERED_CLASS_NAMES = []
RESERVED_CLASS_NAMES = [
    # JavaScript class prototype objects:
    'base_consumer',
    'call',
    'constructor',
    'init',
    '__proto__'
]
RESERVED_ACTION_NAMES = [
    # JavaScript class prototype objects:
    '__proto__'
]


class RegisterEngine(type):
    def __init__(cls, name, bases, attrs):
        if not getattr(cls, 'ACTIONS', None):
            setattr(cls, 'ACTIONS', {})

        for key, val in attrs.items():
            action = getattr(val, '_dce_action', None)
            if action is not None:
                cls.ACTIONS[key] = action

        if not name == 'Engine' and len(cls.ACTIONS.keys()):
            if not name in RESERVED_CLASS_NAMES:
                if not name in REGISTERED_CLASS_NAMES:
                    REGISTERED_CLASS_NAMES.append(name)
                else:
                    raise BadEngine('Engine with name "{}" already registered. Engine names must be unique.'.format(name))
            else:
                raise BadEngine('Engine name "{}" reserved. See: base.RESERVED_CLASS_NAMES.'.format(name))
            ENGINE_CLASSES.append(cls)
