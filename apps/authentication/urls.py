from django.urls import path
from . import views as vw

urlpatterns = [
    path("cordinator-login/", vw.AdminAuthenticationView.as_view(), name="cordinator-login"),
    path("evaluator-login/", vw.EvaluatorAuthenticationView.as_view(), name="evaluator-login")
]
