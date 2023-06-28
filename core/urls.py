from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('platform-admin-panel/', admin.site.urls),
    path("", include("apps.authentication.urls")),
    path("", include("apps.grader.urls"))
]
