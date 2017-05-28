from channels.routing import route

from dcengine.channels_consumers import ws_disconnect, ws_keepalive, ws_connect, ws_receive


routing = [
    route("websocket.connect", ws_connect),
    route("websocket.disconnect", ws_disconnect),
    route("websocket.keepalive", ws_keepalive),
    route("websocket.receive", ws_receive),
]
