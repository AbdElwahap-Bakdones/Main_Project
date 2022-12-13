"""
ASGI config for main_project project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/howto/deployment/asgi/
"""

import os

from channels.routing import ProtocolTypeRouter, URLRouter
from graphene_subscriptions.consumers import GraphqlSubscriptionConsumer
from django.core.asgi import get_asgi_application
from django.urls import path

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "main_project.settings")

django_asgi_app = get_asgi_application()

application = ProtocolTypeRouter({
    "http": django_asgi_app,
    "websocket": URLRouter([
        path(r"graphql/", GraphqlSubscriptionConsumer()),
    ]),
    # Just HTTP for now. (We can add other protocols later.)
})
