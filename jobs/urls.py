from django.urls import path

from .views import (
    JobListCreateView,
    JobDetailView,
    JobBookmarkListCreateView,
    JobBookmarkDeleteView,
)


urlpatterns = [
    path(
        "",
        JobListCreateView.as_view(),
        name="job-list-create"
    ),

    path(
        "<int:pk>/",
        JobDetailView.as_view(),
        name="job-detail"
    ),

    path(
        "bookmarks/",
        JobBookmarkListCreateView.as_view(),
        name="job-bookmarks"
    ),

    path(
        "bookmarks/<int:pk>/",
        JobBookmarkDeleteView.as_view(),
        name="job-bookmark-delete"
    ),
]