from django.urls import path
from . import views as vw


app_name = "authentication"
urlpatterns = [
    path("dev-admin/new-admin/", vw.DevPanelView.as_view()),
    # path("cordinator-login/", vw.AdminAuthenticationView.as_view(), name="asdflogin"),
    path("staff-login/", vw.EvaluatorAuthenticationView.as_view(), name="login"),
    path("logout/", vw.logout_admin, name="logout"),
    path("dashboard/reset/", vw.generate_password_restlink, name="generate-reset-link"),
    path("dashboard/reset/<str:timestamp>/", vw.ResetStaffDetailsView.as_view(), name="reset-details")
]
