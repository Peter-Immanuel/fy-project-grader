from django.contrib import admin
from .models import (
    Faculty,
    Department,
    FinalYearSession,
    Staff,
    Student,
    Project,
    ProjectProposalGrading,
    ProjectWorkProgress,
    InternalDefense,
    ExternalDefense
)
# Register your models here.

admin.site.register([
    Faculty, Department, FinalYearSession, Staff, Student,
    ProjectProposalGrading, ProjectWorkProgress, InternalDefense, 
    ExternalDefense
])


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = ["student", "title", "aims", "objectives", "description"]