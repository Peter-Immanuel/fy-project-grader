from django.urls import path
from . import views as vw


app_name = "authentication"
urlpatterns = [
    path("dev-admin/new-admin/", vw.DevPanelView.as_view()),
    # path("cordinator-login/", vw.AdminAuthenticationView.as_view(), name="asdflogin"),
    path("staff-login/", vw.EvaluatorAuthenticationView.as_view(), name="login"),
    path("logout/", vw.logout_admin, name="logout"),
]
