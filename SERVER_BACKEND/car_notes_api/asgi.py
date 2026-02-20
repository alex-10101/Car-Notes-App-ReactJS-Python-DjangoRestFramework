"""
ASGI config for car_notes_api project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.0/howto/deployment/asgi/
"""

import os

from django.core.asgi import get_asgi_application

# from channels.routing import ProtocolTypeRouter, URLRouter
# from channels.auth import AuthMiddlewareStack
# from channels.security.websocket import AllowedHostsOriginValidator
# import cars.routing

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'car_notes_api.settings')

application = get_asgi_application()

# When integrating with Django channels, and channels must be authenticated:

# # Django's ASGI application to handle traditional HTTP requests
# django_asgi_app = get_asgi_application()

# application = ProtocolTypeRouter(
#     {
#         # HTTP requests are handled by Django as usual
#         "http": django_asgi_app,

#         # WebSocket requests are handled by Channels
#         "websocket": AllowedHostsOriginValidator(
#             AuthMiddlewareStack(
#                 URLRouter(cars.routing.websocket_urlpatterns)
#             )
#         ),
#     }
# )
