import os

from django.core.asgi import get_asgi_application
from channels.routing import ProtocolTypeRouter, URLRouter
from core import routings

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'talkgpt.settings')

application = get_asgi_application()
