from django.conf import settings


DCENGINE_SOCKET_URL_PATH = getattr(settings, 'DCENGINE_SOCKET_URL_PATH', "")
