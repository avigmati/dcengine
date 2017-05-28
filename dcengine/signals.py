from django.dispatch import Signal

user_connect = Signal(providing_args=["user"])
user_disconnect = Signal(providing_args=["user"])
keepalive = Signal()
