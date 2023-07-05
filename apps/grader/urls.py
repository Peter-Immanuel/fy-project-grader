from django.urls import path
from . import views as vw

app_name = "grader"
urlpatterns = [
    path("students/", vw.StudentRegistrationView.as_view(), name="student-registration"),
    path("students/search/", vw.StudentEvaluationSearchView.as_view(), name="search-for-student"),
    path("students/evaluate/proposal/<uuid:student_id>/", vw.ProposalEvaluationView.as_view(), name="proposal-evaluation"),
    path("students/evaluate/work-progress/<uuid:student_id>/", vw.WorkProgressEvaluationView.as_view(), name="work-progress-evaluation"),
    path("students/evaluate/defense/internal/<uuid:student_id>/", vw.InternalDefenseEvaluationView.as_view(), name="internal-defense-evaluation"),
    path("staffs/", vw.StaffRegistrationView.as_view(), name="staff-registration"),
]
