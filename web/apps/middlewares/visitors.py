from os import environ as env

from core.utils import get_user_ip

from .models import visitor


def vistorsMiddleware(get_response):
    def middleware(request):
        ADMIN_URL = env.get("DJANGO_ADMIN_URL", "admin").replace("/", "")  # Get admin url
        IGNORED_PATH = [  # Ignore this paths for logging
            f"/{ADMIN_URL}/jsi18n/",
            f"/{ADMIN_URL}/middlewares/visitor/",
            "/favicon.ico",
        ]

        ip = get_user_ip(request)

        userAgent = request.META.get("HTTP_USER_AGENT")
        path = request.META.get("PATH_INFO")

        if path not in IGNORED_PATH:
            obj = visitor(ip_address=ip, userAgent=userAgent, path=path)
            if path.startswith(f"/{ADMIN_URL}/") and request.user.is_authenticated:
                obj.isAdminPanel = True
            obj.save()

        response = get_response(request)

        return response

    return middleware
