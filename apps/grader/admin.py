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
    list_display = [
        "first_name", "last_name", "matric_number",
        "gender", "session", "proposal_score",
        "work_progress_score", "internal_defense_score", 
        "external_defense_score", "supervisor_score", 
        "hardware_software_score",
    ]
    search_fields = ["first_name", "last_name", "matric_number",]
    list_filter = ["gender", "active", "graduated", "session"]
    
    

@admin.register(ProjectProposalGrading)
class ProjectProposalGradingAdmin(ImportExportActionModelAdmin):
    list_display = [
        "student", "session", "project", "total", "objective_scope", 
        "research_methodology", "literature_review",
        "communication_skills","evaluator", 
        ]
    list_filter = ["evaluator","session",]
    search_fields = ["student", ]


@admin.register(ProjectWorkProgress)
class ProjectWorkProgressAdmin(ImportExportActionModelAdmin):
    list_display = [
        "student", "session", "project",  "total", 
        "project_methodology", "preliminary_result",
        "communication_skills","evaluator", 
        ]
    list_filter = ["evaluator", ]
    search_fields = ["student", ]

@admin.register(InternalDefense)
class InternalDefenseAdmin(ImportExportActionModelAdmin):
    list_filter = ["evaluator", ]
    search_fields = ["student", ]

@admin.register(ExternalDefense)
class ExternalDefenseAdmin(ImportExportActionModelAdmin):
    list_filter = ["evaluator", ]
    search_fields = ["student", ]