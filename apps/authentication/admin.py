from django.contrib import admin
from .models import User
from import_export.admin import ImportExportActionModelAdmin


@admin.register(User)
class UserAdmin(ImportExportActionModelAdmin):
    pass
