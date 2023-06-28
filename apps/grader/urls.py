from django.urls import path
from . import views as vw

urlpatterns = [
    path("students/", vw.StudentDetailsCreationView.as_view(), name="student-details-update"),
]
