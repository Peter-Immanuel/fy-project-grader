from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('platform-admin-panel/', admin.site.urls),
]
