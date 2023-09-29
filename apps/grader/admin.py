from django.contrib import admin
from .models import (
    Faculty,
    Department,
    FinalYearSession,
    Staff, Student,
    Project, ProjectProposalGrading,
    ProjectWorkProgress, InternalDefense,
    ExternalDefense
)
from import_export.admin import ImportExportActionModelAdmin


@admin.register(Project)
class ProjectAdmin(ImportExportActionModelAdmin):
    list_display = [
        "student", "title", "aims", "supervisor", 
        "supervisor_approval", "supervisor_approval_status", "supervisor_comment",
        "cordinator_approval", "cordinator_approval_status", "cordinator_comment"
    ]
    search_fields = [
        "student__first_name", "student__last_name", "student__matric_number", 
        "student__email", "title", "aims", "objectives", "description"
    ]
                     

@admin.register(Staff)
class StaffAdmin(ImportExportActionModelAdmin):
    list_display = ["first_name", "last_name", "staff_type"]

    
@admin.register(Faculty)
class FacultyAdmin(ImportExportActionModelAdmin):
    pass


@admin.register(Department)
class DepartmentAdmin(ImportExportActionModelAdmin):
    pass

@admin.register(FinalYearSession)
class FinalYearSessionAdmin(ImportExportActionModelAdmin):
    pass

@admin.register(Student)
class StudentAdmin(ImportExportActionModelAdmin):
    pass

@admin.register(ProjectProposalGrading)
class ProjectProposalGradingAdmin(ImportExportActionModelAdmin):
    pass

@admin.register(ProjectWorkProgress)
class ProjectWorkProgressAdmin(ImportExportActionModelAdmin):
    pass

@admin.register(InternalDefense)
class InternalDefenseAdmin(ImportExportActionModelAdmin):
    pass

@admin.register(ExternalDefense)
class ExternalDefenseAdmin(ImportExportActionModelAdmin):
    pass