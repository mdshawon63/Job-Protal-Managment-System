from django.urls import path

from .views import (
    CompanyListCreateView,
    CompanyDetailView,
    CompanyVerificationView,
)


urlpatterns = [

    path(
        "",
        CompanyListCreateView.as_view(),
        name="company-list-create"
    ),

    path(
        "<int:pk>/",
        CompanyDetailView.as_view(),
        name="company-detail"
    ),

    path(
        "<int:pk>/verify/",
        CompanyVerificationView.as_view(),
        name="company-verify"
    ),
]