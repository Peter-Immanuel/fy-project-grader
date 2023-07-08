from django.urls import path
from . import views as vw


app_name = "authenticator"
urlpatterns = [
    path("dev-admin/new-admin/", vw.DevPanelView.as_view()),
    path("cordinator-login/", vw.AdminAuthenticationView.as_view(), name="cordinator-login"),
    path("evaluator-login/", vw.EvaluatorAuthenticationView.as_view(), name="evaluator-login")
]
