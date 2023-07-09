from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static


admin.sites.AdminSite.site_header = "FYPG Dev Panel"
admin.sites.AdminSite.site_title = "FYPG Dev Panel"
admin.sites.AdminSite.index_title = "FYPG Dev Panel"


urlpatterns = [
    path('dev-panel/', admin.site.urls),
    path("", include("apps.grader.urls")),
    path("", include("apps.authentication.urls")),
] + static(settings.STATIC_URL, document_root=settings.MEDIA_ROOT)
