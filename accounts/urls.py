from django.urls import path

from .views import (
    RegisterView,
    CandidateProfileView,
    RecruiterProfileView,
    CandidateDashboardView,
    RecruiterDashboardView,
)


urlpatterns = [
    path(
        "register/",
        RegisterView.as_view(),
        name="register"
    ),

    path(
        "candidate/profile/",
        CandidateProfileView.as_view(),
        name="candidate-profile"
    ),

    path(
        "recruiter/profile/",
        RecruiterProfileView.as_view(),
        name="recruiter-profile"
    ),
    path(
    "candidate/dashboard/",
    CandidateDashboardView.as_view(),
    name="candidate-dashboard"
    ),
    path(
    "recruiter/dashboard/",
    RecruiterDashboardView.as_view(),
    name="recruiter-dashboard"),
]