from django.urls import path

from .views import (
    ApplicationListCreateView,
    ApplicationDetailView,
    RecruiterApplicationListView,
    RecruiterApplicationUpdateView,
    InterviewListCreateView,
    InterviewDetailView,
    RecruiterApplicationAnalyticsView,
    JobApplicationAnalyticsView,
)


urlpatterns = [

    path(
        "",
        ApplicationListCreateView.as_view(),
        name="application-list-create"
    ),

    path(
        "<int:pk>/",
        ApplicationDetailView.as_view(),
        name="application-detail"
    ),

    path(
        "recruiter/",
        RecruiterApplicationListView.as_view(),
        name="recruiter-applications"
    ),

    path(
        "recruiter/<int:pk>/",
        RecruiterApplicationUpdateView.as_view(),
        name="recruiter-application-update"
    ),

    path(
        "analytics/",
        RecruiterApplicationAnalyticsView.as_view(),
        name="recruiter-application-analytics"
    ),

    path(
        "analytics/jobs/",
        JobApplicationAnalyticsView.as_view(),
        name="job-application-analytics"
    ),

    path(
        "interviews/",
        InterviewListCreateView.as_view(),
        name="interview-list-create"
    ),

    path(
        "interviews/<int:pk>/",
        InterviewDetailView.as_view(),
        name="interview-detail"
    ),
]