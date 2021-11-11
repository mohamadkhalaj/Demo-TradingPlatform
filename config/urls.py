from django.conf.urls.static import static
from django.urls import path, include
from django.contrib import admin
from django.conf import settings

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('exchange.urls')),
    path('account/', include('account.urls')),
    path('', include('django.contrib.auth.urls')),
    # path('login/', Login.as_view(), name='login'),
    path('', include('social_django.urls', namespace='social')),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)

handler404 = "config.views.page_not_found_view"
handler500 = "config.views.handler500"
handler403 = "config.views.handler403"