import json
from channels.channel import Group

from .base import VERSION, ENGINE_CLASSES, RegisterEngine
from .signals import user_connect, user_disconnect, keepalive
from .request import RequestFactory
from .response import Msg


class Engine(metaclass=RegisterEngine):

    def __init__(self, *args, **kwargs):
        self.request = args[0]
        self.message = self.request.message
        super().__init__()

    @classmethod
    def get_actions(cls):
        actions = []
        for c in ENGINE_CLASSES:
            for a in c.ACTIONS:
                actions.append({'name': '{}.{}'.format(c.__name__, a), 'type': c.ACTIONS[a]['type']})
        return actions

    @classmethod
    def connect(cls, message):
        # send ACK
        msg = Msg(msg_type='service', data={'version': VERSION, 'actions': cls.get_actions()}).json()
        message.reply_channel.send({'text': msg})
        user_connect.send(sender=message, user=message.user)

    @classmethod
    def disconnect(cls, message):
        user_disconnect.send(sender=message, user=message.user)

    @classmethod
    def keepalive(cls, message):
        keepalive.send(sender=message)

    @classmethod
    def dispatch(cls, message):

        msg_content = None

        try:
            msg_content = json.loads(message.content['text'])
        except Exception as e:
            message.reply_channel.send({'text': Msg(error=e.__repr__(), status='error', msg_type='service').json()})
            raise e

        # initialize Request
        try:
            r = RequestFactory(message, msg_content).get_request()
        except Exception as e:
            message.reply_channel.send({'text': Msg(
                error=e.__repr__(),
                error_data=msg_content,
                status='error',
                msg_type='service').json()})
            raise e

        # initialize engine
        try:
            engine = r.engine_class(r)
        except Exception as e:
            msg = Msg(
                cmd_id=getattr(r, 'cmd_id', None),
                consumers=getattr(r, 'callbacks', []),
                status='error',
                error=getattr(e, 'error', e.__repr__()),
                error_data=getattr(e, 'data', None)
            )
            message.reply_channel.send({'text': msg.json()})
            raise e

        # call engine method
        r.engine = engine
        return getattr(engine, r.method_name)(r)

    def add(self, group):
        Group(group).add(self.message.reply_channel)

    def discard(self, group):
        Group(group).discard(self.message.reply_channel)

    def send(self, msg, to=None):
        if not to:
            to = self.message.reply_channel
        to.send({'text': msg.json() if isinstance(msg, Msg) else msg})

    def send_to_group(self, group, msg):
        self.send(msg, to=Group(group))
