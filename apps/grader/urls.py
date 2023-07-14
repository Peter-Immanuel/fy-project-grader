from django.urls import path
from . import views as vw

app_name = "grader"
urlpatterns = [
    
    # App navigation links
    path("", vw.landing_page, name="landing-page"),
    path("students/", vw.student_router, name="student-router"),
    path("staff/", vw.staff_router, name="staff-router"),
    
    
    # Registration liks
    path("staffs/registration/", vw.StaffRegistrationView.as_view(), name="staff-registration"),
    path("students/registration/", vw.StudentRegistrationView.as_view(), name="student-registration"),
    
    
    # Student links 
    path("students/search/", vw.StudentProjectStatus.as_view(), name="student-project-status"),
    path("students/edit-project/<uuid:project_id>/", vw.StudentProjectEditView.as_view(), name="student-project-edit"),
    
    
    
    # student evaluation links
    path("students-evaluation/search/", vw.StudentEvaluationSearchView.as_view(), name="search-for-student"),
    path(
        "students/evaluate/proposal/<uuid:student_id>/", 
        vw.ProposalEvaluationView.as_view(), name="proposal-evaluation"
    ),
    path(
        "students/evaluate/work-progress/<uuid:student_id>/", 
        vw.WorkProgressEvaluationView.as_view(), name="work-progress-evaluation"
    ),
    path(
        "students/evaluate/defense/internal/<uuid:student_id>/", 
        vw.InternalDefenseEvaluationView.as_view(), name="internal-defense-evaluation"
    ),
    path(
        "students/evaluate/defense/external/<uuid:student_id>/", 
        vw.ExternalDefenseEvaluationView.as_view(), name="external-defense-evaluation"
    ),
    
    
    #Staff Dashboard links
    path("staffs/dashboard/", vw.DashboardHomeView.as_view(), name="dashboard"),
    path(
        "staffs/dashboard/students/", vw.DashboardStudentView.as_view(), name="dashboard-student"),
    path(
        "staffs/dashboard/students/<uuid:project_id>/", 
        vw.DashboardStudentDetailView.as_view(), name="dashboard-project-details"
    ),
    path(
        "staffs/dashboard/staffs/", vw.DashboardStaffView.as_view(), name="dashboard-staff"),
    
    path(
        "staffs/dashboard/staffs/students/<uuid:staff_id>/", 
        vw.DashboardStaffStudentsView.as_view(), name="dashboard-staff-students"
    ),
    path("test/", vw.hello)
]
