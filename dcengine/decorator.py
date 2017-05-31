from functools import wraps

from .exceptions import *
from .response import Msg
from .base import RESERVED_ACTION_NAMES


class BaseActionDecorator:
    """
    Base action decorator class
    Checks action declaration
    """
    def __init__(self, f):
        if f.__name__ in RESERVED_ACTION_NAMES:
            raise BadAction('Bad action declaration: {}  is reserved. See: base.RESERVED_ACTION_NAMES.'.format(f.__name__))


class ConsumerAction(BaseActionDecorator):
    """
    Decorator class for Consumer calls
    """

    def __init__(self, f, send=True):
        super().__init__(f)

        self.f = f
        f._dce_action = {'args': ('callbacks', 'data',), 'type': 'consumer', 'send': send}
        wraps(f)(self)

    def __call__(self, request):
        engine = request.engine
        if not getattr(self, '_dce_action')['send']:
            return self.f(engine)
        else:
            e, msg, callbacks = None, None, request.callbacks
            try:
                result = self.f(engine)
            except RequestError as exc:
                e = exc
                msg = Msg(consumers=callbacks, status='error', error=exc.error, error_data=exc.data)
            except Exception as exc:
                e = exc
                msg = Msg(error=exc.__repr__(), consumers=callbacks, status='error')
            else:
                msg = Msg(data=result, consumers=callbacks)
            finally:
                engine.send(msg)
                if e:
                    raise e


def consumer(f=None, send=True):
    """
    Wrapper for Consumer decorator, need to get decorator arguments 
    :param f: Action method
    :param send: 
    :return: 
    """
    if f:
        return ConsumerAction(f)
    else:
        def wrapper(f):
            return ConsumerAction(f, send=send)
        return wrapper


class RpcAction(BaseActionDecorator):
    """
    Decorator class for RPC calls
    """

    def __init__(self, f, send=True):
        super().__init__(f)

        self.f = f
        f._dce_action = {'args': ('cmd_id', 'data',), 'type': 'rpc', 'send': send}
        wraps(f)(self)

    def __call__(self, request):
        engine = request.engine
        if not getattr(self, '_dce_action')['send']:
            return self.f(engine)
        else:
            e, msg, cmd_id = None, None, request.cmd_id
            try:
                result = self.f(engine)
            except RequestError as exc:
                e = exc
                msg = Msg(cmd_id=cmd_id, status='error', error=exc.error, error_data=exc.data)
            except Exception as exc:
                e = exc
                msg = Msg(error=exc.__repr__(), cmd_id=cmd_id, status='error')
            else:
                msg = Msg(data=result, cmd_id=cmd_id)
            finally:
                engine.send(msg)
                if e:
                    raise e


def rpc(f=None, send=True):
    """
    Wrapper for RPC decorator, need to get decorator arguments 
    :param f: Action method
    :param send: 
    :return: 
    """
    if f:
        return RpcAction(f)
    else:
        def wrapper(f):
            return RpcAction(f, send=send)
        return wrapper