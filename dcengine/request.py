from .base import ENGINE_CLASSES
from .exceptions import *


class RequestFactory:
    def __init__(self, message, content):
        self.message = message
        self.content = content
        self.engine_class = None
        self.engine = None
        self.method_name = None
        self._data = ()

        _action = self.content.get('action', None)
        if not _action:
            raise BadRequest('Action not specified.')
        action_class, action_method = _action.split('.')
        for c in ENGINE_CLASSES:
            if c.__name__ == action_class:
                self.engine_class = c
        if not self.engine_class:
            BadRequest('Action class "{}" not found.'.format(action_class))
        try:
            getattr(self.engine_class, action_method)
        except AttributeError:
            raise BadRequest('Action method "{}" of class "{}" not found.'.format(action_method, action_class))

        self.method_name = action_method
        self.method_dict = self.engine_class.ACTIONS.get(action_method)

    def get_request(self):
        if self.method_dict.get('type') == 'consumer':
            return ConsumerRequest(self.message, self.content, self.engine_class, self.method_name, self.method_dict)
        else:
            return RpcRequest(self.message, self.content, self.engine_class, self.method_name, self.method_dict)


class BaseRequest:
    def __init__(self, message, content, engine_class, method_name, method_dict):
        self.message = message
        self.content = content
        self.engine_class = engine_class
        self.method_name = method_name
        self.method_dict = method_dict
        self.engine = None
        self._data = ()
        self.set_args_data()

    def set_args_data(self):
        raise NotImplementedError()


class ConsumerRequest(BaseRequest):
    def __init__(self, *args):
        super().__init__(*args)

    def set_args_data(self):
        for aname in self.method_dict['args']:
            adata = self.content.get(aname, None)
            if aname == 'callbacks':
                if not adata and not adata == []:
                    raise BadRequest('Argument "{}" of method "{}" not specified.'.format(aname, self.method_name))
                adata = list(set(adata))
            else:
                if not adata and not adata == [] and not adata == {}:
                    raise BadRequest('Argument "{}" of method "{}" not specified.'.format(aname, self.method_name))
            self._data += (adata,)
            self.__setattr__(aname, adata)


class RpcRequest(BaseRequest):
    def __init__(self, *args):
        super().__init__(*args)

    def set_args_data(self):
        for aname in self.method_dict['args']:
            adata = self.content.get(aname, None)
            if not adata and not adata == [] and not adata == {}:
                raise BadRequest('Argument "{}" of method "{}" not specified.'.format(aname, self.method_name))
            self._data += (adata,)
            self.__setattr__(aname, adata)