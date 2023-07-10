from django.urls import path
from . import views as vw

app_name = "grader"
urlpatterns = [
    
    # Registration liks
    path("staffs/", vw.StaffRegistrationView.as_view(), name="staff-registration"),
    path("students/", vw.StudentRegistrationView.as_view(), name="student-registration"),
    path("students/search/", vw.StudentEvaluationSearchView.as_view(), name="search-for-student"),
    
    
    # student evaluation links
    path("students/evaluate/proposal/<uuid:student_id>/", vw.ProposalEvaluationView.as_view(), name="proposal-evaluation"),
    path("students/evaluate/work-progress/<uuid:student_id>/", vw.WorkProgressEvaluationView.as_view(), name="work-progress-evaluation"),
    path("students/evaluate/defense/internal/<uuid:student_id>/", vw.InternalDefenseEvaluationView.as_view(), name="internal-defense-evaluation"),
    path("students/evaluate/defense/external/<uuid:student_id>/", vw.ExternalDefenseEvaluationView.as_view(), name="external-defense-evaluation"),
    
    
    path("staffs/dashboard/", vw.DashboardStudentView.as_view(), name=""),
    
    path("test/", vw.hello)
]
