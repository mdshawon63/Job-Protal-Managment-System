from django.contrib import admin
from django.urls import include, path

from accounts.token_views import CustomTokenObtainPairView

from drf_spectacular.views import (
    SpectacularAPIView,
    SpectacularRedocView,
    SpectacularSwaggerView,
)

from rest_framework_simplejwt.views import TokenRefreshView

from .views import (
    home,
    login_page,
    register_page,
    candidate_dashboard,
    recruiter_dashboard,
    job_list,
    job_detail,
    notifications_page,
)


urlpatterns = [

    path(
        "",
        home,
        name="home",
    ),

    path(
        "admin/",
        admin.site.urls,
    ),

    path(
        "login/",
        login_page,
        name="login",
    ),

    path(
        "register/",
        register_page,
        name="register",
    ),

    path(
        "candidate/dashboard/",
        candidate_dashboard,
        name="candidate-dashboard",
    ),

    path(
        "recruiter/dashboard/",
        recruiter_dashboard,
        name="recruiter-dashboard",
    ),

    path(
        "jobs/",
        job_list,
        name="job-list",
    ),

    path(
        "jobs/<int:pk>/",
        job_detail,
        name="job-detail",
    ),

    path(
        "notifications/",
        notifications_page,
        name="notifications",
    ),

    path(
        "api/token/",
        CustomTokenObtainPairView.as_view(),
        name="token_obtain_pair",
    ),

    path(
        "api/token/refresh/",
        TokenRefreshView.as_view(),
        name="token_refresh",
    ),

    path(
        "api/auth/",
        include("accounts.urls"),
    ),

    path(
        "api/companies/",
        include("companies.urls"),
    ),

    path(
        "api/jobs/",
        include("jobs.urls"),
    ),

    path(
        "api/applications/",
        include("applications.urls"),
    ),

    path(
        "api/notifications/",
        include("notifications.urls"),
    ),

    path(
        "api/schema/",
        SpectacularAPIView.as_view(),
        name="schema",
    ),

    path(
        "api/docs/",
        SpectacularSwaggerView.as_view(
            url_name="schema"
        ),
        name="swagger-ui",
    ),

    path(
        "api/redoc/",
        SpectacularRedocView.as_view(
            url_name="schema"
        ),
        name="redoc",
    ),
]