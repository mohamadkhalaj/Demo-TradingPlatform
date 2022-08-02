from account.views import Login, PasswordChange, PasswordReset, Register, activate
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from .views import home

app_name = "config"
urlpatterns = [
    path("", home, name="home"),
    path("login/", Login.as_view(), name="login"),
    path("signup/", Register.as_view(), name="signUp"),
    path("password_reset/", PasswordReset.as_view(), name="password_reset"),
    path("password_change/", PasswordChange.as_view(), name="password_change"),
    path("activate/<uidb64>/<token>/", activate, name="activate"),
    path(settings.ADMIN_URL, admin.site.urls),
    path("admin/", include("admin_honeypot.urls", namespace="admin_honeypot")),
    path("", include("exchange.urls")),
    path("account/", include("account.urls")),
    path("", include("django.contrib.auth.urls")),
    path("", include("social_django.urls", namespace="social")),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "config.views.page_not_found_view"
handler500 = "config.views.handler500"
handler403 = "config.views.handler403"
