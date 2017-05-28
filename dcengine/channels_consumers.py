from channels.auth import channel_session_user, channel_session_user_from_http
from channels.sessions import channel_session

from dcengine import Engine


@channel_session_user_from_http
def ws_connect(message):
    Engine.connect(message)


@channel_session_user
@channel_session
def ws_disconnect(message):
    Engine.disconnect(message)


@channel_session
def ws_keepalive(message):
    Engine.keepalive(message)


@channel_session
@channel_session_user
def ws_receive(message):
    Engine.dispatch(message)
