from exchange.models import visitor


def vistorsMiddleware(get_response):
    def middleware(request):
        IGNORED_PATH = [
            "/admin/jsi18n/",
            "/admin/api/visitor/",
            "/favicon.ico",
        ]

        x_forwarded_for = request.META.get("HTTP_X_FORWARDED_FOR")
        if x_forwarded_for:
            ip = x_forwarded_for.split(",")[0]
        else:
            ip = request.META.get("REMOTE_ADDR")

        userAgent = request.META.get("HTTP_USER_AGENT")
        path = request.META.get("PATH_INFO")

        if path not in IGNORED_PATH:
            obj = visitor(ip_address=ip, userAgent=userAgent, path=path)
            if path.startswith("/admin/"):
                obj.isAdminPanel = True
            obj.save()

        response = get_response(request)

        return response

    return middleware
