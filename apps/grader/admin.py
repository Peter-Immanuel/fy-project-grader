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
    search_fields = [
        "student__first_name", "student__last_name", "student__matric_number", 
        "student__email", "title", "aims", "objectives", "description"
    ]
                     
    

@admin.register(Staff)
class StaffAdmin(admin.ModelAdmin):
    list_display = ["first_name", "last_name", "staff_type"]