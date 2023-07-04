from django.urls import path
from . import views as vw

urlpatterns = [
    path("students/", vw.StudentRegistrationView.as_view(), name="student-registration"),
    path("students/search/", vw.StudentEvaluationSearchView.as_view(), name="search-for-student"),
    path("students/evaluate/<uuid:student_id>/", vw.EvaluationView.as_view(), name="evaluation-form"),
    path("staffs/", vw.StaffRegistrationView.as_view(), name="staff-registration"),
]
