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
    Faculty, Department, FinalYearSession, Student,
    ProjectProposalGrading, ProjectWorkProgress, InternalDefense, 
    ExternalDefense
])


@admin.register(Project)
class ProjectAdmin(admin.ModelAdmin):
    list_display = [
        "student", "title", "aims", 
        "objectives", "description", 
        "supervisor", "supervisor_approval", "supervisor_approval_status", "supervisor_comment",
        "cordinator_approval", "cordinator_approval_status", "cordinator_comment"
    ]
    

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "staff_type"]