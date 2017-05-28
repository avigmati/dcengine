import json

from .utils import serializable


class Msg:
    # todo: rename to Response...

    def __init__(self, data={}, msg_type='user', status='success', cmd_id=None, consumers=[], error=None, error_data=None):
        self.data = data
        self.msg_type = msg_type
        self.status = status
        self.error = error
        self.error_data = error_data
        self.cmd_id = cmd_id
        self.consumers = consumers

    def json(self):
        return json.dumps(serializable({'data': self.data, 'msg_type': self.msg_type, 'status': self.status,
                                        'cmd_id': self.cmd_id, 'consumers': self.consumers,
                                        'error': self.error, 'error_data': self.error_data}))