from django.urls import path
from . import views as vw

urlpatterns = [
    path("students/", vw.StudentRegistrationView.as_view(), name="student-registration"),
    path("students/evaluate/", vw.StudentEvaluationSearchView.as_view(), name="evaluate-student"),
    path("staffs/", vw.StaffRegistrationView.as_view(), name="staff-registration"),
]
