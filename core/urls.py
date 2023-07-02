from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('dev-panel/', admin.site.urls),
    path("", include("apps.grader.urls")),
    path("", include("apps.authentication.urls")),
] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
