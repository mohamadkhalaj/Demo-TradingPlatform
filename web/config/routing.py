import os

import django
from channels.auth import AuthMiddlewareStack
from channels.routing import ProtocolTypeRouter, URLRouter
from channels.security.websocket import AllowedHostsOriginValidator
from channels.sessions import SessionMiddlewareStack

os.environ.setdefault("DJANGO_SETTINGS_MODULE", "config.settings.local")
django.setup()

from account import routing as account_routing
from exchange import routing as exchange_routing
from spot import routing as spot_routing

application = ProtocolTypeRouter(
    {
        "websocket": AllowedHostsOriginValidator(
            SessionMiddlewareStack(
                AuthMiddlewareStack(
                    URLRouter(
                        spot_routing.websocket_urlpatterns
                        + exchange_routing.websocket_urlpatterns
                        + account_routing.websocket_urlpatterns
                    )
                )
            )
        )
    }
)
